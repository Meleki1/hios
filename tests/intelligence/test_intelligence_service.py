import pytest

from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.intelligence_service import (
    IntelligenceService,
)


class FakePredictionService:

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        return Prediction(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )


class FakeEvaluator:

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:

        return PredictionEvaluation(
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            correct=True,
        )


class FakeEvaluationRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        evaluation: PredictionEvaluation,
    ) -> PredictionEvaluation:

        self.saved = evaluation

        return evaluation


@pytest.mark.asyncio
async def test_intelligence_service_predicts():

    service = IntelligenceService(
        prediction_service=FakePredictionService(),
        evaluator=FakeEvaluator(),
        evaluation_repository=FakeEvaluationRepository(),
    )

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    prediction = await service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        intent_score=intent_score,
    )

    assert prediction.subject_id == "household-1"
    assert prediction.target == "pest_control_need"
    assert prediction.horizon_days == 90


@pytest.mark.asyncio
async def test_intelligence_service_evaluates_and_persists():

    repository = FakeEvaluationRepository()

    service = IntelligenceService(
        prediction_service=FakePredictionService(),
        evaluator=FakeEvaluator(),
        evaluation_repository=repository,
    )

    prediction = Prediction(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=[],
        ),
    )

    outcome = Outcome(
        prediction_id=prediction.id,
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    evaluation = await service.evaluate(
        prediction,
        outcome,
    )

    assert evaluation.prediction_id == prediction.id
    assert evaluation.outcome_id == outcome.id
    assert evaluation.correct is True

    assert repository.saved is evaluation

import pytest

from hios.capabilities.intelligence.intelligence_service import (
    IntelligenceService,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)


class FakePredictionService:

    def __init__(self):
        self.received_arguments = None

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        self.received_arguments = {
            "subject_id": subject_id,
            "target": target,
            "horizon_days": horizon_days,
            "intent_score": intent_score,
        }

        return Prediction(
            id="prediction-1",
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
            confidence=0.9,
        )


class FakeEvaluator:

    def __init__(self):
        self.received_prediction = None
        self.received_outcome = None

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:

        self.received_prediction = prediction
        self.received_outcome = outcome

        return PredictionEvaluation(
            id="evaluation-1",
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            correct=outcome.occurred,
        )


class FakeEvaluationRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        evaluation: PredictionEvaluation,
    ) -> PredictionEvaluation:

        self.saved = evaluation

        return evaluation


def make_intent_score() -> IntentScore:

    return IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=0.9,
        signals=[],
    )


def make_prediction() -> Prediction:

    return Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=make_intent_score(),
        confidence=0.9,
    )


def make_outcome(
    occurred: bool = True,
) -> Outcome:

    return Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=occurred,
    )


@pytest.mark.asyncio
async def test_intelligence_service_delegates_prediction():

    prediction_service = FakePredictionService()

    service = IntelligenceService(
        prediction_service=prediction_service,
        evaluator=FakeEvaluator(),
        evaluation_repository=FakeEvaluationRepository(),
    )

    intent_score = make_intent_score()

    result = await service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=intent_score,
    )

    assert result.id == "prediction-1"

    assert result.subject_id == (
        "household-1"
    )

    assert result.target == (
        "pest_control_need"
    )

    assert result.horizon_days == 30

    assert (
        prediction_service.received_arguments[
            "subject_id"
        ]
        == "household-1"
    )

    assert (
        prediction_service.received_arguments[
            "target"
        ]
        == "pest_control_need"
    )

    assert (
        prediction_service.received_arguments[
            "horizon_days"
        ]
        == 30
    )

    assert (
        prediction_service.received_arguments[
            "intent_score"
        ]
        is intent_score
    )


@pytest.mark.asyncio
async def test_intelligence_service_evaluates_prediction():

    evaluator = FakeEvaluator()
    evaluation_repository = FakeEvaluationRepository()

    service = IntelligenceService(
        prediction_service=FakePredictionService(),
        evaluator=evaluator,
        evaluation_repository=evaluation_repository,
    )

    prediction = make_prediction()
    outcome = make_outcome(
        occurred=True,
    )

    result = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.id == "evaluation-1"

    assert result.prediction_id == (
        prediction.id
    )

    assert result.outcome_id == (
        outcome.id
    )

    assert result.correct is True

    assert (
        evaluator.received_prediction
        is prediction
    )

    assert (
        evaluator.received_outcome
        is outcome
    )

    assert (
        evaluation_repository.saved
        is result
    )