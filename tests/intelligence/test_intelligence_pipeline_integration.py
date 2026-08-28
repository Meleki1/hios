import pytest

from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.providers.mock import (
    MockEnvironmentalProvider,
)
from hios.capabilities.environmental.service import (
    EnvironmentalService,
)
from hios.capabilities.intelligence.basic_signal_engine import (
    BasicSignalEngine,
)
from hios.capabilities.intelligence.collectors.conversation import (
    ConversationSignalCollector,
)
from hios.capabilities.intelligence.collectors.environmental import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.collectors.explicit_intent import (
    ExplicitIntentCollector,
)
from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)
from hios.capabilities.intelligence.collectors.platform import (
    PlatformBehaviourSignalCollector,
)
from hios.capabilities.intelligence.collectors.property import (
    PropertySignalCollector,
)
from hios.capabilities.intelligence.intelligence_pipeline import (
    IntelligencePipeline,
)
from hios.capabilities.intelligence.intelligence_service import (
    IntelligenceService,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.prediction_engine import (
    PredictionEngine,
)
from hios.capabilities.intelligence.prediction_service import (
    PredictionService,
)
from hios.capabilities.intelligence.signal_collection_service import (
    SignalCollectionService,
)
from hios.capabilities.property.providers.mock import (
    MockPropertyProvider,
)
from hios.capabilities.property.service import (
    PropertyService,
)
from hios.capabilities.local_activity.local_activity_service import (
    LocalActivityService,
)

from hios.capabilities.local_activity.local_activity_aggregator import (
    LocalActivityAggregator,
)

from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)

from hios.capabilities.local_activity.providers.mock_planning_application_provider import (
    MockPlanningApplicationProvider,
)


class FakePredictionEngine(PredictionEngine):

    def __init__(self):
        self.received = None

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        self.received = {
            "subject_id": subject_id,
            "target": target,
            "horizon_days": horizon_days,
            "intent_score": intent_score,
        }

        return Prediction(
            id="prediction-integration-1",
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )


class FakePredictionRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        prediction: Prediction,
    ) -> Prediction:

        self.saved = prediction
        return prediction

@pytest.mark.asyncio
async def test_intelligence_pipeline_integrates_signals_intent_and_prediction():

    signal_engine = BasicSignalEngine(
        explicit_intent_collector=ExplicitIntentCollector(),
        conversation_collector=ConversationSignalCollector(),
        property_collector=PropertySignalCollector(),
        environmental_collector=EnvironmentalSignalCollector(),
        local_activity_collector=LocalActivitySignalCollector(),
        platform_behaviour_collector=(
            PlatformBehaviourSignalCollector()
        ),
    )

    property_service = PropertyService(
        provider=MockPropertyProvider(),
    )

    environmental_service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    local_activity_service = LocalActivityService(
        providers=[
            MockPlanningApplicationProvider(),
        ],
    )

    local_activity_aggregator = (
        LocalActivityAggregator()
    )

    local_activity_signal_collector = (
        LocalActivitySignalCollector()
    )

    signal_collection_service = SignalCollectionService(
        signal_engine=signal_engine,
        intent_scorer=RuleBasedIntentScorer(),
        property_service=property_service,
        environmental_service=environmental_service,
        local_activity_service=(
            local_activity_service
        ),
        local_activity_aggregator=(
            local_activity_aggregator
        ),
        local_activity_signal_collector=(
            local_activity_signal_collector
        ),
    )

    prediction_engine = FakePredictionEngine()

    prediction_repository = FakePredictionRepository()

    prediction_service = PredictionService(
        engine=prediction_engine,
        repository=prediction_repository,
    )

    intelligence_service = IntelligenceService(
        prediction_service=prediction_service,
        evaluator=None,
        evaluation_repository=None,
    )

    pipeline = IntelligencePipeline(
        signal_collection_service=(
            signal_collection_service
        ),
        intelligence_service=intelligence_service,
    )

    property_profile = await property_service.get_property(
        "100023456789",
    )

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    prediction = await pipeline.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        property_profile=property_profile,
        environmental_observation=observation,
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "asked_about_pests",
        ],
        local_activities={
            "local_pest_reports": "increasing",
        },
        platform_behaviours={
            "return_visits": "3",
        },
    )

    assert prediction.id == (
        "prediction-integration-1"
    )

    assert prediction.subject_id == (
        "household-1"
    )

    assert prediction.target == (
        "pest_control_need"
    )

    assert prediction.horizon_days == 14

    assert prediction.intent_score.score == 25.0

    assert prediction.intent_score.level == (
        IntentLevel.LOW
    )

    assert len(
        prediction.intent_score.signals
    ) > 0

    assert any(
        signal.value == "reported_active_problem"
        for signal in prediction.intent_score.signals
    )

    assert prediction_engine.received is not None

    assert (
        prediction_engine.received["intent_score"]
        is prediction.intent_score
    )

    assert (
        prediction_repository.saved
        is prediction
    )