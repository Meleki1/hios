from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.memory.models.memory_entry import MemoryEntry


class MemoryFormation(ABC):

    @abstractmethod
    async def extract(
        self,
        learning: Learning,
    ) -> list[MemoryEntry]:
        raise NotImplementedError