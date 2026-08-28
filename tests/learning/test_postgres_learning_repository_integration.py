import pytest
from sqlalchemy import delete
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.postgres.repository import (
    PostgresLearningRepository,
)
from hios.capabilities.learning.postgres.models.learning_record import (
    LearningRecordModel,
)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_learning_repository_persists_and_retrieves(
    session,
):
    await session.execute(
        delete(LearningRecordModel).where(
            LearningRecordModel.prediction_id
            == "prediction-learning-1"
        )
    )

    await session.commit()

    record = LearningRecord(
        prediction_id="prediction-learning-1",
        outcome_id="outcome-learning-1",
        evaluation_id="evaluation-learning-1",
        target="pest_control_need",
        correct=True,
        signal_names=[
            "requested_treatment",
            "price_inquiry",
        ],
        signal_values=[
            "pest_control",
            "treatment_price",
        ],
        signal_strengths=[
            1.0,
            0.8,
        ],
        signal_confidences=[
            1.0,
            0.9,
        ],
        intent_score=75.0,
        prediction_confidence=0.9,
        lesson="Prediction was correct.",
    )

    repository = PostgresLearningRepository(
        session=session,
    )

    saved = await repository.save(
        record,
    )

    assert saved.id == record.id

    retrieved = (
        await repository.get_by_prediction(
            "prediction-learning-1",
        )
    )

    assert retrieved is not None

    assert retrieved.id == record.id
    assert retrieved.prediction_id == (
        record.prediction_id
    )
    assert retrieved.outcome_id == (
        record.outcome_id
    )
    assert retrieved.evaluation_id == (
        record.evaluation_id
    )
    assert retrieved.target == record.target
    assert retrieved.correct is True

    assert retrieved.signal_names == (
        record.signal_names
    )

    assert retrieved.signal_values == (
        record.signal_values
    )

    assert retrieved.signal_strengths == (
        record.signal_strengths
    )

    assert retrieved.signal_confidences == (
        record.signal_confidences
    )

    assert retrieved.intent_score == (
        record.intent_score
    )

    assert retrieved.prediction_confidence == (
        record.prediction_confidence
    )

    assert retrieved.lesson == (
        record.lesson
    )