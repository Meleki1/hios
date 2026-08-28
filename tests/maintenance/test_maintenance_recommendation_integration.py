import pytest

from hios.capabilities.maintenance.models.maintenance import (
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.services.maintenance_recommendation_service import (
    MaintenanceRecommendationService,
)
from datetime import datetime, timezone

from hios.capabilities.maintenance.services.maintenance_timeline_planner import (
    MaintenanceTimelinePlanner,
)
from hios.capabilities.maintenance.services.maintenance_intelligence_service import (
    MaintenanceIntelligenceService,
)
from hios.capabilities.maintenance.services.maintenance_recommendation_service import (
    MaintenanceRecommendationService,
)
from tests.maintenance.test_maintenance_intelligence_service import FakeMaintenanceTimelinePlanner, FakeRecommendationScheduler, FakePatternDetector, FakeHistoryExtractor, FakeIntelligencePipeline

class FakeMaintenanceRepository:

    def __init__(self):
        self.records = []

    async def create(self, maintenance):
        self.records.append(maintenance)
        return maintenance

    async def find_active_by_task(
        self,
        *,
        home_id,
        task,
    ):
        for record in self.records:
            if (
                record.home_id == home_id
                and record.task == task
                and record.status in (
                    MaintenanceStatus.PLANNED,
                    MaintenanceStatus.DUE,
                )
            ):
                return record

        return None


@pytest.mark.asyncio
async def test_accepting_recommendation_persists_maintenance():

    repository = FakeMaintenanceRepository()

    service = MaintenanceRecommendationService(
        maintenance_repository=repository,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        priority="normal",
    )

    maintenance = await service.accept(
        recommendation=recommendation,
    )

    assert len(repository.records) == 1

    persisted = repository.records[0]

    assert persisted is maintenance
    assert persisted.subject_id == "household-1"
    assert persisted.home_id == "home-1"
    assert persisted.task == "Pest inspection"
    assert (
        persisted.maintenance_type
        == MaintenanceType.PREVENTIVE
    )
    assert (
        persisted.status
        == MaintenanceStatus.PLANNED
    )



@pytest.mark.asyncio
async def test_accepted_recommendation_appears_in_maintenance_timeline():

    repository = FakeMaintenanceRepository()

    service = MaintenanceRecommendationService(
        maintenance_repository=repository,
    )

    recommended_for = datetime(
        2026,
        9,
        15,
        10,
        30,
        tzinfo=timezone.utc,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        recommended_for=recommended_for,
    )

    maintenance = await service.accept(
        recommendation=recommendation,
    )

    planner = MaintenanceTimelinePlanner()

    timeline = await planner.build(
        subject_id="household-1",
        home_id="home-1",
        maintenance_records=[
            maintenance,
        ],
        recommendations=[],
    )

    assert len(timeline) == 1

    assert timeline[0].task == "Pest inspection"

    assert (
        timeline[0].scheduled_for
        == recommended_for
    )

@pytest.mark.asyncio
async def test_accepted_maintenance_is_visible_to_future_assistant_analysis():

    repository = FakeMaintenanceRepository()

    recommendation_service = MaintenanceRecommendationService(
        maintenance_repository=repository,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        priority="normal",
    )

    # First cycle:
    # Accept the recommendation and persist maintenance.
    maintenance = await recommendation_service.accept(
        recommendation=recommendation,
    )

    assert len(repository.records) == 1
    assert repository.records[0] is maintenance

    # Second cycle:
    # The persisted maintenance is supplied to maintenance intelligence.
    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()
    scheduler = FakeRecommendationScheduler()

    intelligence_service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        recommendation_scheduler=scheduler,
        timeline_planner=FakeMaintenanceTimelinePlanner(),
    )

    result = await intelligence_service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=["timeline-event"],
        maintenance_records=repository.records,
    )

   
    assert result.recommendations == []
