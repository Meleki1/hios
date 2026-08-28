import pytest

from hios.capabilities.intelligence.basic_prediction_evaluator import (
    BasicPredictionEvaluator,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentLevel,
    IntentScore,
)
from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)


def make_prediction() -> Prediction:

    return Prediction(
        id="prediction-feedback-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=[],
        ),
    )


@pytest.mark.asyncio
async def test_prediction_feedback_flow_marks_prediction_correct():

    prediction = make_prediction()

    outcome = Outcome(
        prediction_id=prediction.id,
        subject_id=prediction.subject_id,
        target=prediction.target,
        occurred=True,
    )

    evaluator = BasicPredictionEvaluator()

    evaluation = await evaluator.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert evaluation.prediction_id == (
        prediction.id
    )

    assert evaluation.outcome_id == (
        outcome.id
    )

    assert evaluation.correct is True


@pytest.mark.asyncio
async def test_prediction_feedback_flow_marks_prediction_incorrect():

    prediction = make_prediction()

    outcome = Outcome(
        prediction_id=prediction.id,
        subject_id=prediction.subject_id,
        target=prediction.target,
        occurred=False,
    )

    evaluator = BasicPredictionEvaluator()

    evaluation = await evaluator.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert evaluation.prediction_id == (
        prediction.id
    )

    assert evaluation.outcome_id == (
        outcome.id
    )

    assert evaluation.correct is False

@pytest.mark.asyncio
async def test_prediction_feedback_flow_rejects_wrong_prediction():

    prediction = make_prediction()

    outcome = Outcome(
        prediction_id="different-prediction",
        subject_id=prediction.subject_id,
        target=prediction.target,
        occurred=True,
    )

    evaluator = BasicPredictionEvaluator()

    evaluation = await evaluator.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert evaluation.correct is False