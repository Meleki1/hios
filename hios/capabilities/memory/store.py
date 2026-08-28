from abc import ABC, abstractmethod

from hios.capabilities.memory.models.memory_entry import MemoryEntry


class MemoryStore(ABC):

    @abstractmethod
    async def store(
        self,
        memories: list[MemoryEntry],
    ) -> list[MemoryEntry]:
        raise NotImplementedError

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.70,
        category: str | None = None,
    ) -> list[MemoryEntry]:
        raise NotImplementedError