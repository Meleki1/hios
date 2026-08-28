import pytest

from hios.capabilities.intelligence.basic_prediction_evaluator import (
    BasicPredictionEvaluator,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction


def make_prediction(
    prediction_id: str = "prediction-1",
    target: str = "pest_control_need",
) -> Prediction:

    return Prediction(
        id=prediction_id,
        subject_id="household-1",
        target=target,
        horizon_days=14,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=[],
        ),
    )


def make_outcome(
    prediction_id: str = "prediction-1",
    target: str = "pest_control_need",
    occurred: bool = True,
) -> Outcome:

    return Outcome(
        prediction_id=prediction_id,
        subject_id="household-1",
        target=target,
        occurred=occurred,
    )


@pytest.mark.asyncio
async def test_evaluator_marks_occurred_prediction_correct():

    prediction = make_prediction()
    outcome = make_outcome()

    evaluator = BasicPredictionEvaluator()

    result = await evaluator.evaluate(
        prediction,
        outcome,
    )

    assert result.prediction_id == prediction.id
    assert result.outcome_id == outcome.id
    assert result.correct is True


@pytest.mark.asyncio
async def test_evaluator_marks_non_occurred_prediction_incorrect():

    prediction = make_prediction()

    outcome = make_outcome(
        occurred=False,
    )

    evaluator = BasicPredictionEvaluator()

    result = await evaluator.evaluate(
        prediction,
        outcome,
    )

    assert result.correct is False


@pytest.mark.asyncio
async def test_evaluator_rejects_mismatched_target():

    prediction = make_prediction(
        target="pest_control_need",
    )

    outcome = make_outcome(
        target="flood_risk",
        occurred=True,
    )

    evaluator = BasicPredictionEvaluator()

    result = await evaluator.evaluate(
        prediction,
        outcome,
    )

    assert result.correct is False


@pytest.mark.asyncio
async def test_evaluator_requires_matching_prediction_id():

    prediction = make_prediction(
        prediction_id="prediction-1",
    )

    outcome = make_outcome(
        prediction_id="prediction-2",
    )

    evaluator = BasicPredictionEvaluator()

    result = await evaluator.evaluate(
        prediction,
        outcome,
    )

    assert result.correct is False