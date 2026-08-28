from abc import ABC, abstractmethod

from hios.capabilities.memory.models.memory_entry import MemoryEntry


class MemoryDeduplicator(ABC):

    @abstractmethod
    async def is_duplicate(
        self,
        memory: MemoryEntry,
    ) -> bool:
        raise NotImplementedError