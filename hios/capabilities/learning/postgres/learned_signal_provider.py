from hios.capabilities.learning.learned_signal_provider import (
    LearnedSignalProvider,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)
from hios.capabilities.learning.postgres.learning_insight_repository import (
    PostgresLearningInsightRepository,
)


class PostgresLearnedSignalProvider(
    LearnedSignalProvider,
):

    def __init__(
        self,
        repository: PostgresLearningInsightRepository,
    ):
        self._repository = repository

    async def get_signal_performance(
        self,
        target: str,
        signal_name: str,
    ) -> SignalPerformance | None:

        insights = await self._repository.get_all()

        for insight in insights:
            if (
                insight.target == target
                and insight.signal_name == signal_name
            ):
                return SignalPerformance(
                    sample_size=insight.sample_size,
                    correct_count=round(
                        insight.sample_size
                        * insight.accuracy
                    ),
                    incorrect_count=(
                        insight.sample_size
                        - round(
                            insight.sample_size
                            * insight.accuracy
                        )
                    ),
                    accuracy=insight.accuracy,
                )

        return None