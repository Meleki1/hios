from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class LearningRepository(ABC):

    @abstractmethod
    async def save(
        self,
        record: LearningRecord,
    ) -> LearningRecord:
        raise NotImplementedError

    @abstractmethod
    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> LearningRecord | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
    ) -> list[LearningRecord]:
        raise NotImplementedError