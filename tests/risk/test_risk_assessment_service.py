import pytest

from hios.capabilities.risk.models.risk_score import (
    RiskLevel,
    RiskScore,
)
from hios.capabilities.risk.risk_assessment_service import (
    RiskAssessmentService,
)
from hios.capabilities.intelligence.prediction_service import (
    PredictionService,
)
from hios.capabilities.risk.rule_based_risk_engine import (
    RuleBasedRiskEngine,
)
from hios.capabilities.risk.risk_service import (
    RiskService,
)
from hios.capabilities.risk.risk_signal_adapter import (
    RiskSignalAdapter,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.prediction_engine import PredictionEngine
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
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

class FakeRiskService:

    def __init__(self):
        self.received = []

    async def assess(
        self,
        **kwargs,
    ) -> RiskScore:

        self.received.append(kwargs)

        scores = {
            "pest": 65.0,
            "flood": 40.0,
            "damp": 20.0,
        }

        score = scores.get(
            kwargs["risk_type"],
            0.0,
        )

        if score >= 70:
            level = RiskLevel.HIGH
        elif score >= 40:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return RiskScore(
            risk_type=kwargs["risk_type"],
            score=score,
            level=level,
            confidence=1.0,
        )


@pytest.mark.asyncio
async def test_risk_assessment_service_assesses_multiple_risks():

    risk_service = FakeRiskService()

    service = RiskAssessmentService(
        risk_service=risk_service,
    )

    result = await service.assess(
        risk_types=[
            "pest",
            "flood",
            "damp",
        ],
        property_characteristics={
            "year_built": "1890",
        },
        environmental_observations={
            "rainfall": "42.0",
        },
    )

    assert len(result.risks) == 3

    assert result.risks[0].risk_type == "pest"
    assert result.risks[0].score == 65.0

    assert result.risks[1].risk_type == "flood"
    assert result.risks[1].score == 40.0

    assert result.risks[2].risk_type == "damp"
    assert result.risks[2].score == 20.0

    assert len(risk_service.received) == 3

    assert (
        risk_service.received[0]["property_characteristics"]
        == {"year_built": "1890"}
    )

    assert (
        risk_service.received[0]["environmental_observations"]
        == {"rainfall": "42.0"}
    )

@pytest.mark.asyncio
async def test_risk_signals_flow_into_prediction():

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

    assessment = (
        await risk_assessment_service.assess(
            risk_types=[
                "flood",
                "pest",
            ],
            property_characteristics={
                "flood_risk": "high",
            },
            environmental_observations={
                "rainfall": "50",
            },
        )
    )

    assert len(assessment.risks) == 2

    assert (
        assessment.risks[0].risk_type
        == "flood"
    )

    assert (
        assessment.risks[1].risk_type
        == "pest"
    )

    # --------------------------------------------------
    # Risk → Signals
    # --------------------------------------------------

    risk_signal_adapter = (
        RiskSignalAdapter()
    )

    risk_signals = (
        risk_signal_adapter.to_signals(
            assessment,
        )
    )

    assert len(risk_signals) == 2

    assert any(
        signal.name == "flood_risk"
        for signal in risk_signals
    )

    assert any(
        signal.name == "pest_risk"
        for signal in risk_signals
    )

    # --------------------------------------------------
    # Intent
    # --------------------------------------------------

    intent_scorer = (
        RuleBasedIntentScorer()
    )

    intent_score = (
        await intent_scorer.score(
            risk_signals,
        )
    )

    assert intent_score is not None

    assert (
        len(intent_score.signals)
        == 2
    )

    assert any(
        signal.name == "flood_risk"
        for signal in intent_score.signals
    )

    assert any(
        signal.name == "pest_risk"
        for signal in intent_score.signals
    )

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------

    prediction_engine = (
        FakePredictionEngine()
    )

    prediction_repository = (
        FakePredictionRepository()
    )

    prediction_service = (
        PredictionService(
            engine=prediction_engine,
            repository=prediction_repository,
        )
    )

    prediction = (
        await prediction_service.predict(
            subject_id="household-1",
            target="pest_control_need",
            horizon_days=14,
            intent_score=intent_score,
        )
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert prediction is not None

    assert (
        prediction.subject_id
        == "household-1"
    )

    assert (
        prediction.target
        == "pest_control_need"
    )

    assert (
        prediction.horizon_days
        == 14
    )

    assert (
        prediction.intent_score
        is intent_score
    )

    assert (
        prediction_repository.saved
        is prediction
    )

    assert (
        prediction_engine.received
        is not None
    )

    assert (
        prediction_engine.received[
            "intent_score"
        ]
        is intent_score
    )