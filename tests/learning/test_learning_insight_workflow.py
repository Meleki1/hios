import pytest

from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)
from hios.capabilities.learning.workflow import (
    LearningInsightWorkflow,
)


class FakeLearningAnalyzer:

    def __init__(self):
        self.received_records = None

    async def analyze(
        self,
        records: list[LearningRecord],
    ) -> list[LearningPattern]:

        self.received_records = records

        return [
            LearningPattern(
                target="pest_control_need",
                sample_size=2,
                correct_count=2,
                incorrect_count=0,
                accuracy=1.0,
                lesson=(
                    "Predictions for pest_control_need "
                    "were correct 100.0% of the time."
                ),
                signal_performance={
                    "asked_about_pests": SignalPerformance(
                        sample_size=2,
                        correct_count=2,
                        incorrect_count=0,
                        accuracy=1.0,
                    ),
                },
            )
        ]


class FakeLearningInsightGenerator:

    def __init__(self):
        self.received_patterns = None

    async def generate(
        self,
        pattern: LearningPattern,
    ) -> list[LearningInsight]:

        if self.received_patterns is None:
            self.received_patterns = []

        self.received_patterns.append(pattern)

        return [
            LearningInsight(
                target="pest_control_need",
                signal_name="asked_about_pests",
                sample_size=2,
                correct_count=1,
                incorrect_count=1,
                accuracy=0.5,
                insight=(
                    "asked_about_pests "
                    "was correct 50.0% of the time."
                ),
            )
        ]


class FakeLearningInsightRepository:

    def __init__(self):
        self.saved = []

    async def save(
        self,
        insight: LearningInsight,
    ) -> LearningInsight:

        self.saved.append(insight)

        return insight


def make_record() -> LearningRecord:
    return LearningRecord(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        evaluation_id="evaluation-1",
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


@pytest.mark.asyncio
async def test_learning_insight_workflow_analyzes_and_persists():

    analyzer = FakeLearningAnalyzer()
    generator = FakeLearningInsightGenerator()
    repository = FakeLearningInsightRepository()

    workflow = LearningInsightWorkflow(
        analyzer=analyzer,
        insight_generator=generator,
        insight_repository=repository,
    )

    records = [
        make_record(),
    ]

    result = await workflow.process(
        records,
    )

    assert len(result) == 1

    assert result[0].target == (
        "pest_control_need"
    )

    assert result[0].signal_name == (
        "asked_about_pests"
    )

    assert analyzer.received_records is records

    assert len(
        generator.received_patterns
    ) == 1

    assert (
        generator.received_patterns[0].target
        == "pest_control_need"
    )

    assert len(repository.saved) == 1

    assert repository.saved[0] is result[0]
    assert result[0].sample_size == 2
    assert result[0].correct_count == 1
    assert result[0].incorrect_count == 1
    assert result[0].accuracy == 0.5