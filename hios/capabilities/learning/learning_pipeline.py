from hios.capabilities.learning.learning_analyzer import LearningAnalyzer
from hios.capabilities.learning.learning_insight_generator import (
    LearningInsightGenerator,
)
from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class LearningPipeline:

    def __init__(
        self,
        analyzer: LearningAnalyzer,
        insight_generator: LearningInsightGenerator,
        insight_repository,
    ):
        self._analyzer = analyzer
        self._insight_generator = insight_generator
        self._insight_repository = insight_repository

    async def process(
        self,
        records: list[LearningRecord],
    ) -> list[LearningInsight]:

        patterns = await self._analyzer.analyze(
            records,
        )

        insights = self._insight_generator.generate(
            patterns,
        )

        persisted_insights = []

        for insight in insights:
            saved = await self._insight_repository.save(
                insight,
            )
            persisted_insights.append(saved)

        return persisted_insights