from abc import ABC, abstractmethod

from hios.capabilities.memory.models.memory_entry import MemoryEntry


class MemoryConsolidator(ABC):

    @abstractmethod
    async def consolidate(
        self,
        memories: list[MemoryEntry],
    ) -> MemoryEntry:
        raise NotImplementedError