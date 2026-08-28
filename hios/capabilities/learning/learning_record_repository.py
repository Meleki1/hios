from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class LearningRecordRepository(ABC):

    @abstractmethod
    async def get_all(
        self,
    ) -> list[LearningRecord]:
        ...