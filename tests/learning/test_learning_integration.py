import pytest

from hios.capabilities.learning.basic_learning_analyzer import (
    BasicLearningAnalyzer,
)
from hios.capabilities.learning.insight_generator import (
    BasicLearningInsightGenerator,
)
from hios.capabilities.learning.learning_pipeline import (
    LearningPipeline,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class FakeLearningInsightRepository:
    def __init__(self):
        self.saved = []

    async def save(self, insight):
        self.saved.append(insight)
        return insight


def make_record(
    prediction_id: str,
    correct: bool,
    signal_name: str = "asked_about_pests",
) -> LearningRecord:

    return LearningRecord(
        prediction_id=prediction_id,
        outcome_id=f"outcome-{prediction_id}",
        evaluation_id=f"evaluation-{prediction_id}",
        target="pest_control_need",
        correct=correct,
        signal_names=[signal_name],
        signal_values=["pest_control"],
        signal_strengths=[1.0],
        signal_confidences=[0.9],
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson=(
            "Prediction was correct."
            if correct
            else "Prediction was incorrect."
        ),
    )


@pytest.mark.asyncio
async def test_learning_pipeline_end_to_end():

    analyzer = BasicLearningAnalyzer()

    generator = BasicLearningInsightGenerator()

    repository = FakeLearningInsightRepository()

    pipeline = LearningPipeline(
        analyzer=analyzer,
        insight_generator=generator,
        insight_repository=repository,
    )

    records = [
        make_record(
            "prediction-1",
            True,
        ),
        make_record(
            "prediction-2",
            True,
        ),
        make_record(
            "prediction-3",
            False,
        ),
        make_record(
            "prediction-4",
            True,
        ),
        make_record(
            "prediction-5",
            True,
        ),
    ]

    result = await pipeline.process(
        records,
    )

    assert len(result) == 1

    insight = result[0]

    assert insight.target == (
        "pest_control_need"
    )

    assert insight.signal_name == (
        "asked_about_pests"
    )

    assert insight.sample_size == 5

    assert insight.correct_count == 4

    assert insight.incorrect_count == 1

    assert insight.accuracy == 0.8

    assert insight.insight == (
        "The signal asked_about_pests "
        "was associated with pest_control_need "
        "being correct 80.0% of the time."
    )

    assert len(repository.saved) == 1

    assert repository.saved[0] is insight