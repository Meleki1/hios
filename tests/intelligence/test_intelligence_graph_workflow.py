import pytest
from hios.capabilities.intelligence.graph.workflow import build_intelligence_graph
from hios.capabilities.intelligence.models.intent_level import IntentLevel
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.risk.models.risk_score import RiskLevel, RiskScore
from hios.capabilities.risk.models.risk_assessment import RiskAssessment

from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
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
from hios.capabilities.intelligence.graph.workflow import (
    build_intelligence_graph,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import RuleBasedIntentScorer
from hios.capabilities.intelligence.intelligence_service import (
    IntelligenceService,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
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
from hios.capabilities.environmental.providers.mock import (
    MockEnvironmentalProvider,
)
from hios.capabilities.environmental.service import (
    EnvironmentalService,
)
from hios.capabilities.risk.rule_based_risk_engine import (
    RuleBasedRiskEngine,
)
from hios.capabilities.risk.risk_assessment_service import (
    RiskAssessmentService,
)
from hios.capabilities.risk.risk_service import (
    RiskService,
)
from hios.capabilities.risk.risk_signal_adapter import (
    RiskSignalAdapter,
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
from hios.capabilities.local_activity.providers.planning_applications import (
    MockPlanningApplicationProvider,
)
from hios.capabilities.intelligence.graph.workflow import (
    build_intelligence_graph,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.signal import (
    Signal,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)

class ExplicitIntentSignalCollectionFake:

    async def collect(
        self,
        subject_id,
        property_profile=None,
        environmental_observation=None,
        explicit_intents=None,
        interactions=None,
        local_activities=None,
        platform_behaviours=None,
        radius_km=5.0,
        include_local_activity=True,
    ):

        signals = []

        for intent in explicit_intents or []:

            signals.append(
                Signal(
                    type=SignalType.EXPLICIT_INTENT,
                    source=SignalSource.HOME_ASSIST,
                    name="explicit_intent",
                    value=intent,
                    strength=1.0,
                    confidence=1.0,
                )
            )

        return signals

    async def score_signals(
        self,
        signals,
    ):

        return IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=signals,
        )

    async def collect_local_activity_with_status(
        self,
        subject_id,
        property_profile,
        radius_km=5.0,
    ):
        return [], []


class FakeRiskAssessmentService:

    async def assess(
        self,
        risk_types,
        property_characteristics=None,
        environmental_observations=None,
    ):

        return FakeRiskAssessment()


class FakeRiskSignalAdapter:

    def to_signals(
        self,
        assessment,
    ):

        return []


class ExplicitIntentIntelligenceServiceFake:

    def __init__(self):
        self.called = False

    async def predict(
        self,
        subject_id,
        target,
        horizon_days,
        intent_score,
    ):

        self.called = True

        return Prediction(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )


class FakeRiskAssessment:

    risks = []


class FakePredictionEngine:

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score,
    ) -> Prediction:

        return Prediction(
            id="prediction-e2e-1",
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


class FakeSignalCollectionService:

    def __init__(self):
        self.received = None
        self.scored_signals = None

    async def collect(self, **kwargs):

        self.received = kwargs

        return []

    async def score_signals(self, signals):

        self.scored_signals = signals

        return IntentScore(
            score=75.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=signals,
        )


class FakeIntelligenceService:

    async def predict(self, **kwargs):

        return Prediction(
            id="graph-prediction-1",
            subject_id=kwargs["subject_id"],
            target=kwargs["target"],
            horizon_days=kwargs["horizon_days"],
            intent_score=kwargs["intent_score"],
        )

class FakeRiskAssessmentService:

    async def assess(self, **kwargs):
        return RiskAssessment(
            risks=[
                RiskScore(
                    risk_type="pest",
                    score=30.0,
                    level=RiskLevel.LOW,
                    confidence=1.0,
                ),
            ],
        )


class FakeRiskSignalAdapter:

    def to_signals(self, assessment):
        return []


@pytest.mark.asyncio
async def test_intelligence_graph_collects_and_predicts():

    graph = build_intelligence_graph(
        signal_collection_service=(
            FakeSignalCollectionService()
        ),
        intelligence_service=(
            FakeIntelligenceService()
        ),
        risk_assessment_service=(
            FakeRiskAssessmentService()
        ),
        risk_signal_adapter=(
            FakeRiskSignalAdapter()
        ),
    )

    result = await graph.ainvoke(
        {
            "subject_id": "household-1",
            "target": "pest_control_need",
            "horizon_days": 14,
            "explicit_intents": [
                "reported_active_problem",
            ],
        }
    )

    assert result["intent_score"].score == 75.0

    assert (
        result["intent_score"].level
        == IntentLevel.HIGH
    )

    assert result["prediction"].id == (
        "graph-prediction-1"
    )

    assert result["prediction"].subject_id == (
        "household-1"
    )

    assert result["prediction"].target == (
        "pest_control_need"
    )


@pytest.mark.asyncio
async def test_intelligence_graph_end_to_end():

    # --------------------------------------------------
    # Property
    # --------------------------------------------------

    property_service = PropertyService(
        provider=MockPropertyProvider(),
    )

    property_profile = (
        await property_service.get_property(
            "100023456789",
        )
    )

    assert property_profile is not None

    # --------------------------------------------------
    # Environmental
    # --------------------------------------------------

    environmental_service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    environmental_observation = (
        EnvironmentalObservation(
            rainfall_mm=42.0,
            temperature_c=18.5,
            humidity_percent=78.0,
            wind_speed_mps=4.2,
            frost=False,
        )
    )

    # --------------------------------------------------
    # Local Activity
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Signal collection
    # --------------------------------------------------

    signal_engine = BasicSignalEngine(
        explicit_intent_collector=(
            ExplicitIntentCollector()
        ),
        conversation_collector=(
            ConversationSignalCollector()
        ),
        property_collector=(
            PropertySignalCollector()
        ),
        environmental_collector=(
            EnvironmentalSignalCollector()
        ),
        local_activity_collector=(
            LocalActivitySignalCollector()
        ),
        platform_behaviour_collector=(
            PlatformBehaviourSignalCollector()
        ),
    )

    signal_collection_service = (
        SignalCollectionService(
            signal_engine=signal_engine,
            intent_scorer=RuleBasedIntentScorer(),
            property_service=property_service,
            environmental_service=(
                environmental_service
            ),
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
    )

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    risk_engine = RuleBasedRiskEngine()

    risk_service = RiskService(
        engine=risk_engine,
    )

    risk_assessment_service = (
        RiskAssessmentService(
            risk_service=risk_service,
        )
    )

    risk_signal_adapter = (
        RiskSignalAdapter()
    )

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------

    prediction_engine = FakePredictionEngine()

    prediction_repository = (
        FakePredictionRepository()
    )

    prediction_service = PredictionService(
        engine=prediction_engine,
        repository=prediction_repository,
    )

    intelligence_service = IntelligenceService(
        prediction_service=prediction_service,
        evaluator=None,
        evaluation_repository=None,
    )

    # --------------------------------------------------
    # Graph
    # --------------------------------------------------

    graph = build_intelligence_graph(
        signal_collection_service=(
            signal_collection_service
        ),
        intelligence_service=(
            intelligence_service
        ),
        risk_assessment_service=(
            risk_assessment_service
        ),
        risk_signal_adapter=(
            risk_signal_adapter
        ),
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    result = await graph.ainvoke(
        {
            "subject_id": "household-e2e-1",
            "target": "pest_control_need",
            "horizon_days": 14,
            "property_profile": property_profile,
            "environmental_observation": (
                environmental_observation
            ),
            "explicit_intents": [
                "reported_active_problem",
            ],
            "interactions": [
                "asked_about_pests",
            ],
            "local_activities": {
                "local_pest_reports": "increasing",
            },
            "platform_behaviours": {
                "return_visits": "3",
            },
        }
    )

    # --------------------------------------------------
    # Risk assertions
    # --------------------------------------------------
    assert property_profile.latitude is not None
    assert property_profile.longitude is not None
    assert result["risk_assessment"] is not None

    assert len(
        result["risk_assessment"].risks
    ) == 2

    assert len(
        result["risk_signals"]
    ) == 2

    # --------------------------------------------------
    # Intent assertions
    # --------------------------------------------------

    assert result["intent_score"] is not None

    assert (
        result["intent_score"].score
        == 25.0
    )

    assert len(
        result["intent_score"].signals
    ) > 6

    assert any(
        signal.value
        == "reported_active_problem"
        for signal in result["intent_score"].signals
    )

    assert any(
        signal.name == "pest_risk"
        for signal in result["intent_score"].signals
    )

    assert any(
        signal.name == "flood_risk"
        for signal in result["intent_score"].signals
    )

    # --------------------------------------------------
    # Local Activity assertions
    # --------------------------------------------------

    assert any(
        signal.type.value == "local_activity"
        for signal in result["intent_score"].signals
    )

    assert any(
        signal.name
        == "local_activity_restaurant"
        for signal in result["intent_score"].signals
    )

    # --------------------------------------------------
    # Prediction assertions
    # --------------------------------------------------

    prediction = result["prediction"]

    assert prediction is not None

    assert prediction.id == (
        "prediction-e2e-1"
    )

    assert prediction.subject_id == (
        "household-e2e-1"
    )

    assert prediction.target == (
        "pest_control_need"
    )

    assert prediction.horizon_days == 14

    assert (
        prediction.intent_score
        is result["intent_score"]
    )

    assert (
        prediction_repository.saved
        is prediction
    )

@pytest.mark.asyncio
async def test_intelligence_graph_runs_risk_signals_score_and_prediction():

    signal_collection_service = (
        ExplicitIntentSignalCollectionFake()
    )

    intelligence_service = (
        ExplicitIntentIntelligenceServiceFake()
    )

    graph = build_intelligence_graph(
        signal_collection_service=(
            signal_collection_service
        ),
        intelligence_service=(
            intelligence_service
        ),
        risk_assessment_service=(
            FakeRiskAssessmentService()
        ),
        risk_signal_adapter=(
            FakeRiskSignalAdapter()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "target": "home_maintenance",
        "horizon_days": 30,
        "explicit_intents": [
            "requested_treatment",
            "asked_for_price",
        ],
    }

    result = await graph.ainvoke(
        state,
    )

    assert result["intent_score"] is not None

    assert (
        result["intent_score"].level
        == IntentLevel.HIGH
    )

    assert result["prediction"] is not None

    assert (
        result["prediction"].subject_id
        == "subject-123"
    )

    assert (
        result["prediction"].target
        == "home_maintenance"
    )

    assert (
        result["prediction"].horizon_days
        == 30
    )

    assert intelligence_service.called is True

    print(
        "INTENT SCORE:",
        result["intent_score"],
    )