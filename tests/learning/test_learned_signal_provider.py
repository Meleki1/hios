import pytest

from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.postgres.learned_signal_provider import (
    PostgresLearnedSignalProvider,
)


class FakeLearningInsightRepository:

    def __init__(self, insights):
        self.insights = insights

    async def get_all(self):
        return self.insights


@pytest.mark.asyncio
async def test_provider_returns_signal_performance():

    repository = FakeLearningInsightRepository(
        [
            LearningInsight(
                target="pest_control_need",
                signal_name="asked_about_pests",
                sample_size=4,
                correct_count=3,
                incorrect_count=1,
                accuracy=0.75,
                insight=(
                    "asked_about_pests "
                    "was correct 75.0% of the time."
                ),
            ),
        ]
    )

    provider = PostgresLearnedSignalProvider(
        repository,
    )

    result = await provider.get_signal_performance(
        target="pest_control_need",
        signal_name="asked_about_pests",
    )

    assert result is not None
    assert result.sample_size == 4
    assert result.correct_count == 3
    assert result.incorrect_count == 1
    assert result.accuracy == 0.75


@pytest.mark.asyncio
async def test_provider_returns_none_for_unknown_signal():

    repository = FakeLearningInsightRepository(
        []
    )

    provider = PostgresLearnedSignalProvider(
        repository,
    )

    result = await provider.get_signal_performance(
        target="pest_control_need",
        signal_name="unknown_signal",
    )

    assert result is None