import pytest
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.graph.nodes import collect_and_score, predict
from hios.capabilities.intelligence.graph.state import IntelligenceState
from hios.capabilities.intelligence.models.intent_level import IntentLevel
from hios.capabilities.intelligence.graph.nodes import assess_risk
from hios.capabilities.risk.models.risk_assessment import RiskAssessment
from hios.capabilities.risk.models.risk_score import RiskLevel, RiskScore
from hios.capabilities.intelligence.models.signal_source import SignalSource
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.intent_score import IntentScore



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
            score=25.0,
            level=IntentLevel.LOW,
            confidence=1.0,
            signals=signals,
        )


@pytest.mark.asyncio
async def test_collect_and_score_node():

    service = FakeSignalCollectionService()

    state: IntelligenceState = {
        "subject_id": "household-1",
        "target": "pest_control_need",
        "horizon_days": 14,
        "explicit_intents": [
            "reported_active_problem",
        ],
        "interactions": [
            "asked_about_pests",
        ],
    }

    result = await collect_and_score(
        state=state,
        signal_collection_service=service,
    )

    assert result["intent_score"].score == 25.0

    assert (
        result["intent_score"].level
        == IntentLevel.LOW
    )

    assert (
        service.received["subject_id"]
        == "household-1"
    )

    assert (
        service.received["explicit_intents"]
        == ["reported_active_problem"]
    )

    assert (
        service.received["interactions"]
        == ["asked_about_pests"]
    )

@pytest.mark.asyncio
async def test_predict_node():

    from hios.capabilities.intelligence.models.intent_score import (
        IntentScore,
    )

    from hios.capabilities.intelligence.models.prediction import (
        Prediction,
    )

    class FakeIntelligenceService:

        def __init__(self):
            self.received = None

        async def predict(
            self,
            **kwargs,
        ):

            self.received = kwargs

            return Prediction(
                id="prediction-node-1",
                subject_id=kwargs["subject_id"],
                target=kwargs["target"],
                horizon_days=kwargs["horizon_days"],
                intent_score=kwargs["intent_score"],
            )

    intelligence_service = FakeIntelligenceService()

    intent_score = IntentScore(
        score=75.0,
        level=IntentLevel.HIGH,
        confidence=0.9,
        signals=[],
    )

    state: IntelligenceState = {
        "subject_id": "household-1",
        "target": "pest_control_need",
        "horizon_days": 14,
        "intent_score": intent_score,
    }

    result = await predict(
        state=state,
        intelligence_service=intelligence_service,
    )

    assert result["prediction"].id == (
        "prediction-node-1"
    )

    assert (
        intelligence_service.received["subject_id"]
        == "household-1"
    )

    assert (
        intelligence_service.received["target"]
        == "pest_control_need"
    )

    assert (
        intelligence_service.received["horizon_days"]
        == 14
    )

    assert (
        intelligence_service.received["intent_score"]
        is intent_score
    )


@pytest.mark.asyncio
async def test_assess_risk_node():

    class FakeRiskAssessmentService:

        def __init__(self):
            self.received = None

        async def assess(
            self,
            **kwargs,
        ):

            self.received = kwargs

            return RiskAssessment(
                risks=[
                    RiskScore(
                        risk_type="pest",
                        score=30.0,
                        level=RiskLevel.LOW,
                        confidence=1.0,
                    ),
                    RiskScore(
                        risk_type="flood",
                        score=70.0,
                        level=RiskLevel.HIGH,
                        confidence=0.9,
                    ),
                ],
            )

    class FakeRiskSignalAdapter:

        def __init__(self):
            self.received = None

        def to_signals(
            self,
            assessment,
        ):

            self.received = assessment

            return [
                "risk-signal-1",
                "risk-signal-2",
            ]

    risk_service = FakeRiskAssessmentService()
    adapter = FakeRiskSignalAdapter()

    state: IntelligenceState = {
        "subject_id": "household-1",
        "target": "pest_control_need",
        "horizon_days": 14,
        "property_profile": None,
        "environmental_observation": None,
    }

    result = await assess_risk(
        state=state,
        risk_assessment_service=risk_service,
        risk_signal_adapter=adapter,
    )

    assert isinstance(
        result["risk_assessment"],
        RiskAssessment,
    )

    assert len(
        result["risk_assessment"].risks
    ) == 2

    assert result["risk_signals"] == [
        "risk-signal-1",
        "risk-signal-2",
    ]

    assert (
        risk_service.received["risk_types"]
        == ["pest", "flood"]
    )

    assert (
        adapter.received
        is result["risk_assessment"]
    )

@pytest.mark.asyncio
async def test_collect_and_score_includes_risk_signals():

    class FakeSignalCollectionService:

        def __init__(self):
            self.scored_signals = None

        async def collect(self, **kwargs):
            return []

        async def score_signals(self, signals):

            self.scored_signals = signals

            return IntentScore(
                score=25.0,
                level=IntentLevel.LOW,
                confidence=1.0,
                signals=signals,
            )

    service = FakeSignalCollectionService()

    risk_signal = Signal(
        type=SignalType.ENVIRONMENTAL,
        source=SignalSource.PROPERTY,
        name="flood_risk",
        value="high",
        strength=0.7,
        confidence=0.9,
    )

    state: IntelligenceState = {
        "subject_id": "household-1",
        "target": "pest_control_need",
        "horizon_days": 14,
        "risk_signals": [
            risk_signal,
        ],
    }

    result = await collect_and_score(
        state=state,
        signal_collection_service=service,
    )

    assert risk_signal in service.scored_signals

    assert risk_signal in (
        result["intent_score"].signals
    )