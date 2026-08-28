import pytest

from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.learning_repository import (
    LearningRepository,
)


class FakeLearningRepository(LearningRepository):

    def __init__(self):
        self.records = []

    async def save(
        self,
        record: LearningRecord,
    ) -> LearningRecord:
        self.records.append(record)
        return record

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> LearningRecord | None:
        for record in self.records:
            if record.prediction_id == prediction_id:
                return record

        return None

    async def get_all(
        self,
    ) -> list[LearningRecord]:
        return self.records

@pytest.mark.asyncio
async def test_learning_repository_saves_record():

    repository = FakeLearningRepository()

    record = LearningRecord(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        evaluation_id="evaluation-1",
        target="pest_control_need",
        correct=True,
        signal_names=[
            "requested_treatment",
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

    result = await repository.save(record)

    assert result is record
    assert repository.records == [
        record,
    ]

@pytest.mark.asyncio
async def test_learning_repository_gets_record_by_prediction():

    repository = FakeLearningRepository()

    record = LearningRecord(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        evaluation_id="evaluation-1",
        target="pest_control_need",
        correct=True,
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson="Prediction was correct.",
    )

    await repository.save(record)

    result = await repository.get_by_prediction(
        "prediction-1",
    )

    assert result is record

@pytest.mark.asyncio
async def test_learning_repository_returns_none_for_unknown_prediction():

    repository = FakeLearningRepository()

    result = await repository.get_by_prediction(
        "prediction-unknown",
    )

    assert result is None