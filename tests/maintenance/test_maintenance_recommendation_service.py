import pytest

from hios.capabilities.maintenance.models.maintenance import (
    MaintenanceStatus,
    MaintenanceType,
    Maintenance
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.services.maintenance_recommendation_service import (
    MaintenanceRecommendationService,
)
from datetime import datetime, timezone


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
async def test_accept_recommendation_creates_maintenance_record():

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

    assert maintenance.subject_id == "household-1"
    assert maintenance.home_id == "home-1"
    assert maintenance.task == "Pest inspection"

    assert (
        maintenance.maintenance_type
        == MaintenanceType.PREVENTIVE
    )

    assert (
        maintenance.status
        == MaintenanceStatus.PLANNED
    )

    assert repository.records == [maintenance]

@pytest.mark.asyncio
async def test_accept_recommendation_does_not_duplicate_existing_maintenance():

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )

    repository = FakeMaintenanceRepository()
    repository.records.append(existing)

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

    assert maintenance is existing
    assert len(repository.records) == 1

@pytest.mark.asyncio
async def test_accept_recommendation_creates_new_maintenance_after_completion():

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.COMPLETED,
    )

    repository = FakeMaintenanceRepository()
    repository.records.append(existing)

    service = MaintenanceRecommendationService(
        maintenance_repository=repository,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="New pest-related concerns were detected.",
        priority="normal",
    )

    maintenance = await service.accept(
        recommendation=recommendation,
    )

    assert maintenance is not existing
    assert maintenance.task == "Pest inspection"
    assert maintenance.status == MaintenanceStatus.PLANNED
    assert len(repository.records) == 2

@pytest.mark.asyncio
async def test_accept_recommendation_preserves_recommended_date():

    recommended_for = datetime(
        2026,
        9,
        15,
        10,
        30,
        tzinfo=timezone.utc,
    )

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
        recommended_for=recommended_for,
    )

    maintenance = await service.accept(
        recommendation=recommendation,
    )

    assert maintenance.scheduled_for == recommended_for

