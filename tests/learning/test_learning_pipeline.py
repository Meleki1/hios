import pytest

from hios.capabilities.learning.learning_pipeline import (
    LearningPipeline,
)
from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)


class FakeAnalyzer:

    def __init__(self):
        self.received_records = None

    async def analyze(self, records):
        self.received_records = records
        return ["pattern-1"]


class FakeInsightGenerator:

    def __init__(self):
        self.received_patterns = None

    def generate(self, patterns):
        self.received_patterns = patterns

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
            ),
        ]


class FakeInsightRepository:

    def __init__(self):
        self.saved = []

    async def save(self, insight):
        self.saved.append(insight)
        return insight


@pytest.mark.asyncio
async def test_learning_pipeline_analyzes_generates_and_persists():

    analyzer = FakeAnalyzer()
    generator = FakeInsightGenerator()
    repository = FakeInsightRepository()

    pipeline = LearningPipeline(
        analyzer=analyzer,
        insight_generator=generator,
        insight_repository=repository,
    )

    records = [
        "record-1",
        "record-2",
    ]

    result = await pipeline.process(
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

    assert generator.received_patterns == [
        "pattern-1",
    ]

    assert repository.saved == result

    assert repository.saved[0] is result[0]