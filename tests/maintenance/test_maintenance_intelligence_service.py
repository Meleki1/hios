import pytest

from hios.capabilities.maintenance.services.maintenance_intelligence_service import (
    MaintenanceIntelligenceService,
)
from hios.capabilities.maintenance.intelligence.maintenance_pattern_detector import (
    MaintenancePatternDetector,
)
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
)
from hios.capabilities.maintenance.intelligence.maintenance_history import MaintenanceHistorySignalExtractor
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.services.maintenance_recommendation_scheduler import (
    MaintenanceRecommendationScheduler,
)
from datetime import datetime, timedelta, timezone



class FakeHistoryExtractor:

    def __init__(self):
        self.received_timeline = None

    def extract(self, timeline):
        self.received_timeline = timeline

        return [
            "pest signal",
        ]

class FakePattern:

    def __init__(
        self,
        category,
        occurrences,
        descriptions,
    ):
        self.category = category
        self.occurrences = occurrences
        self.descriptions = descriptions

class FakeRecommendationScheduler:

    def __init__(self):
        self.calls = []

    def schedule(
        self,
        *,
        now,
        horizon_days,
    ):
        self.calls.append(
            {
                "now": now,
                "horizon_days": horizon_days,
            }
        )

        return now

class FakePatternDetector:

    def __init__(self):
        self.received_signals = None

    def detect(self, signals):
        self.received_signals = signals

        return [
            FakePattern(
                category="pest",
                occurrences=3,
                descriptions=[
                    "Asked about mice",
                    "Reported seeing mice again",
                    "Requested pest inspection",
                ],
            )
        ]

class FakeMaintenanceTimelinePlanner:

    def __init__(self):
        self.timeline = []

    async def build(
        self,
        *,
        subject_id,
        home_id,
        maintenance_records,
        recommendations,
    ):
        return self.timeline

class FakeIntelligencePipeline:

    def __init__(self):
        self.calls = []

    async def predict(self, **kwargs):
        self.calls.append(kwargs)

        return {
            "prediction": "maintenance_needed",
        }

class IntelligencePipelineFake:

    def __init__(self):
        self.calls = []

    async def predict(
        self,
        *,
        subject_id,
        target,
        horizon_days,
        property_profile=None,
        environmental_observation=None,
        explicit_intents=None,
        interactions=None,
        local_activities=None,
        platform_behaviours=None,
    ):
        self.calls.append(
            {
                "subject_id": subject_id,
                "target": target,
                "horizon_days": horizon_days,
                "property_profile": property_profile,
                "environmental_observation": (
                    environmental_observation
                ),
                "explicit_intents": explicit_intents,
                "interactions": interactions,
                "local_activities": local_activities,
                "platform_behaviours": platform_behaviours,
            }
        )

        return object()


@pytest.mark.asyncio
async def test_maintenance_intelligence_uses_intelligence_pipeline():

    pipeline = IntelligencePipelineFake()

    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=[],
        maintenance_records=[],
        property_profile=None,
        environmental_observation=None,
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[],
        local_activities=[],
        platform_behaviours=[],
    )

    assert len(pipeline.calls) == 1

    call = pipeline.calls[0]

    assert call["subject_id"] == "household-1"
    assert call["target"] == "home_maintenance"
    assert call["horizon_days"] == 30

    assert call["explicit_intents"] == [
        "reported_active_problem",
    ]


@pytest.mark.asyncio
async def test_maintenance_intelligence_recommends_pest_inspection():

    pipeline = IntelligencePipelineFake()

    extractor = MaintenanceHistorySignalExtractor()
    detector = MaintenancePatternDetector()

    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )   

        

    timeline = [
        type(
            "TimelineEntry",
            (),
            {
                "event_name": "message_received",
                "description": "Asked about mice",
                "subject_id": "household-1",
                "resource_id": "conversation-1",
                "resource_type": "conversation",
                "created_at": None,
            },
        )(),
        type(
            "TimelineEntry",
            (),
            {
                "event_name": "message_received",
                "description": "Asked about wasps",
                "subject_id": "household-1",
                "resource_id": "conversation-2",
                "resource_type": "conversation",
                "created_at": None,
            },
        )(),
        type(
            "TimelineEntry",
            (),
            {
                "event_name": "message_received",
                "description": "Requested pest inspection",
                "subject_id": "household-1",
                "resource_id": "conversation-3",
                "resource_type": "conversation",
                "created_at": None,
            },
        )(),
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1

    recommendation = result.recommendations[0]

    assert recommendation.task == (
        "Pest inspection"
    )

    assert recommendation.maintenance_type == (
        "preventive"
    )

    assert recommendation.subject_id == (
        "household-1"
    )

    assert recommendation.home_id == (
        "home-1"
    )

    assert recommendation.priority == "normal"

    assert len(
        recommendation.source_signals
    ) == 3



@pytest.mark.asyncio
async def test_maintenance_intelligence_uses_intelligence_pipeline():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    await service.analyze(
        subject_id="household-1",
        home_id="home-1",
    )

    assert len(pipeline.calls) == 1

    call = pipeline.calls[0]

    assert call["subject_id"] == "household-1"
    assert call["target"] == "home_maintenance"
    assert call["horizon_days"] == 30


@pytest.mark.asyncio
async def test_maintenance_intelligence_extracts_history_from_timeline():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert history_extractor.received_timeline == timeline


@pytest.mark.asyncio
async def test_maintenance_intelligence_passes_history_to_pattern_detector():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=[
            "timeline-event",
        ],
    )

    assert pattern_detector.received_signals == [
        "pest signal",
    ]


@pytest.mark.asyncio
async def test_maintenance_intelligence_builds_pest_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1


    recommendation = result.recommendations[0]

    assert recommendation.subject_id == "household-1"
    assert recommendation.home_id == "home-1"

    assert recommendation.task == "Pest inspection"
    assert recommendation.maintenance_type == "preventive"
    assert recommendation.priority == "normal"

    assert recommendation.reason == (
        "Repeated pest-related concerns were identified "
        "in the home history."
    )

    assert recommendation.source_signals == [
        "Asked about mice",
        "Reported seeing mice again",
        "Requested pest inspection",
    ]

    assert recommendation.metadata == {
        "pattern": "pest",
        "occurrences": "3",
    }

@pytest.mark.asyncio
async def test_maintenance_intelligence_passes_all_intelligence_inputs():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        property_profile={"property_type": "house"},
        environmental_observation={
            "weather": "wet",
        },
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "conversation-1",
        ],
        local_activities=[
            "pest_activity",
        ],
        platform_behaviours=[
            "inspection_search",
        ],
    )

    call = pipeline.calls[0]

    assert call["property_profile"] == {
        "property_type": "house",
    }

    assert call["environmental_observation"] == {
        "weather": "wet",
    }

    assert call["explicit_intents"] == [
        "reported_active_problem",
    ]

    assert call["interactions"] == [
        "conversation-1",
    ]

    assert call["local_activities"] == [
        "pest_activity",
    ]

    assert call["platform_behaviours"] == [
        "inspection_search",
    ]

@pytest.mark.asyncio
async def test_maintenance_intelligence_does_not_duplicate_existing_maintenance():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing_maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        status="planned",
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
        maintenance_records=[
            existing_maintenance,
        ],
    )

    assert result.recommendations == []

@pytest.mark.asyncio
async def test_planned_maintenance_suppresses_duplicate_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        status="planned",
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
        maintenance_records=[
            existing,
        ],
    )

    assert result.recommendations == []

@pytest.mark.asyncio
async def test_completed_maintenance_does_not_immediately_duplicate():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        status="completed",
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
        maintenance_records=[
            existing,
        ],
    )

    assert result.recommendations == []

@pytest.mark.asyncio
async def test_maintenance_on_different_home_does_not_suppress_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-2",
        task="Pest inspection",
        maintenance_type="preventive",
        status="planned",
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
        maintenance_records=[
            existing,
        ],
    )



    assert len(result.recommendations) == 1

    recommendation = result.recommendations[0]

    assert recommendation.task == "Pest inspection"
    assert recommendation.home_id == "home-1"

@pytest.mark.asyncio
async def test_different_maintenance_task_does_not_suppress_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()


    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Gutter cleaning",
        maintenance_type="preventive",
        status="planned",
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
        maintenance_records=[
            existing,
        ],
    )

    assert len(result.recommendations) == 1
    recommendation = result.recommendations[0]
    assert recommendation.task == "Pest inspection"

@pytest.mark.asyncio
async def test_overdue_maintenance_allows_new_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.OVERDUE,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1

    recommendation = result.recommendations[0]

    assert recommendation.task == "Pest inspection"
    assert recommendation.home_id == "home-1"

@pytest.mark.asyncio
async def test_cancelled_maintenance_allows_new_recommendation():
    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()

    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.CANCELLED,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1

    

    assert result.recommendations[0].task == "Pest inspection"

@pytest.mark.asyncio
async def test_maintenance_recommendation_has_recommended_date():
    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()
    scheduler = MaintenanceRecommendationScheduler()

    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()
    
    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1

    

    recommendation = result.recommendations[0]

    assert recommendation.task == "Pest inspection"
    assert recommendation.recommended_for is not None


@pytest.mark.asyncio
async def test_maintenance_intelligence_schedules_recommendation():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()
    scheduler = MaintenanceRecommendationScheduler()
    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()

    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        #recommendation_scheduler=scheduler,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    timeline = [
        "timeline-event-1",
        "timeline-event-2",
    ]

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=timeline,
    )

    assert len(result.recommendations) == 1

    

    recommendation = result.recommendations[0]

    assert recommendation.task == "Pest inspection"
    assert recommendation.recommended_for is not None

@pytest.mark.asyncio
async def test_maintenance_intelligence_builds_timeline():

    pipeline = FakeIntelligencePipeline()
    history_extractor = FakeHistoryExtractor()
    pattern_detector = FakePatternDetector()
    recommendation_scheduler = FakeRecommendationScheduler()
    timeline_planner = FakeMaintenanceTimelinePlanner()

    service = MaintenanceIntelligenceService(
        intelligence_pipeline=pipeline,
        history_extractor=history_extractor,
        pattern_detector=pattern_detector,
        recommendation_scheduler=recommendation_scheduler,
        timeline_planner=timeline_planner,
    )

    result = await service.analyze(
        subject_id="household-1",
        home_id="home-1",
        timeline=["timeline-event"],
    )

    assert result.timeline == (
        timeline_planner.timeline
    )