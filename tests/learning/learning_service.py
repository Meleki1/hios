import pytest

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
from hios.capabilities.learning.learning_service import (
    LearningService,
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
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


def make_learning_record(
    prediction_id: str,
) -> LearningRecord:
    return LearningRecord(
        prediction_id=prediction_id,
        outcome_id=f"outcome-{prediction_id}",
        evaluation_id=f"evaluation-{prediction_id}",
        target="pest_control_need",
        correct=True,
        signal_names=[
            "asked_about_pests",
        ],
        signal_values=[
            "pest_control",
        ],
        signal_strengths=[
            1.0,
        ],
        signal_confidences=[
            1.0,
        ],
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson="Prediction was correct.",
    )

def make_prediction() -> Prediction:

    return Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=[],
        ),
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


def make_evaluation(
    correct: bool = True,
) -> PredictionEvaluation:

    return PredictionEvaluation(
        id="evaluation-1",
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        correct=correct,
    )


@pytest.mark.asyncio
async def test_learning_service_creates_learning_record():

    service = LearningService()

    prediction = make_prediction()

    outcome = make_outcome(
        occurred=True,
    )

    evaluation = make_evaluation(
        correct=True,
    )

    result = await service.learn_from_prediction(
        prediction=prediction,
        outcome=outcome,
        evaluation=evaluation,
    )

    assert result.prediction_id == (
        prediction.id
    )

    assert result.outcome_id == (
        outcome.id
    )

    assert result.evaluation_id == (
        evaluation.id
    )

    assert result.target == (
        prediction.target
    )

    assert result.correct is True

    assert result.intent_score == 70.0

    assert result.prediction_confidence == 0.9

@pytest.mark.asyncio
async def test_learning_service_creates_correct_prediction_lesson():

    service = LearningService()

    result = await service.learn_from_prediction(
        prediction=make_prediction(),
        outcome=make_outcome(
            occurred=True,
        ),
        evaluation=make_evaluation(
            correct=True,
        ),
    )

    assert result.lesson == (
        "Prediction was correct."
    )


@pytest.mark.asyncio
async def test_learning_service_creates_incorrect_prediction_lesson():

    service = LearningService()

    result = await service.learn_from_prediction(
        prediction=make_prediction(),
        outcome=make_outcome(
            occurred=False,
        ),
        evaluation=make_evaluation(
            correct=False,
        ),
    )

    assert result.correct is False

    assert result.lesson == (
        "Prediction was incorrect."
    )

@pytest.mark.asyncio
async def test_learning_service_preserves_prediction_signals():

    service = LearningService()

    signals = [
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="requested_treatment",
            value="pest_control",
            strength=1.0,
            confidence=1.0,
        ),
        Signal(
            type=SignalType.CONVERSATION,
            source=SignalSource.HOME_ASSIST,
            name="interaction",
            value="asked_about_treatment_price",
            strength=0.8,
            confidence=0.9,
        ),
    ]

    prediction = Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=signals,
        ),
        confidence=0.9,
    )

    result = await service.learn_from_prediction(
        prediction=prediction,
        outcome=make_outcome(),
        evaluation=make_evaluation(),
    )

    assert result.signal_names == [
        "requested_treatment",
        "interaction",
    ]

    assert result.signal_values == [
        "pest_control",
        "asked_about_treatment_price",
    ]

    assert result.signal_strengths == [
        1.0,
        0.8,
    ]

    assert result.signal_confidences == [
        1.0,
        0.9,
    ]

from hios.capabilities.learning.postgres.repository import PostgresLearningRepository
@pytest.mark.asyncio
async def test_learning_repository_gets_all_records(
    session,
):
    repository = PostgresLearningRepository(
        session,
    )

    record_1 = make_learning_record(
        prediction_id="prediction-1",
    )

    record_2 = make_learning_record(
        prediction_id="prediction-2",
    )

    await repository.save(record_1)
    await repository.save(record_2)

    records = await repository.get_all()

    prediction_ids = {
        record.prediction_id
        for record in records
    }

    assert "prediction-1" in prediction_ids
    assert "prediction-2" in prediction_ids