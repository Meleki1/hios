from hios.capabilities.learning.learning_analyzer import (
    LearningAnalyzer,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.learning_repository import (
    LearningRepository,
)


class LearningAnalysisService:

    def __init__(
        self,
        repository: LearningRepository,
        analyzer: LearningAnalyzer,
    ):
        self._repository = repository
        self._analyzer = analyzer

    async def analyze(
        self,
    ) -> list[LearningPattern]:

        records = await self._repository.get_all()

        return await self._analyzer.analyze(
            records,
        )