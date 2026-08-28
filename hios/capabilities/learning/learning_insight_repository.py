from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)


class LearningInsightRepository(ABC):

    @abstractmethod
    async def save(
        self,
        insight: LearningInsight,
    ) -> LearningInsight:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
    ) -> list[LearningInsight]:
        raise NotImplementedError