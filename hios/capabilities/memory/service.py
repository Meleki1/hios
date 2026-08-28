from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.memory.deduplication import (
    MemoryDeduplicator,
)
from hios.capabilities.memory.formation import MemoryFormation
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.store import MemoryStore


class MemoryService:

    def __init__(
        self,
        store: MemoryStore,
        formation: MemoryFormation,
        deduplicator: MemoryDeduplicator,
    ):
        self._store = store
        self._formation = formation
        self._deduplicator = deduplicator

    async def remember(
        self,
        learning: Learning,
    ) -> list[MemoryEntry]:

        candidates = await self._formation.extract(
            learning,
        )

        memories: list[MemoryEntry] = []

        for memory in candidates:

            if await self._deduplicator.is_duplicate(
                memory,
            ):
                continue

            memories.append(memory)

        if not memories:
            return []

        return await self._store.store(
            memories,
        )

    async def recall(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.70,
        category: str | None = None,
    ) -> list[MemoryEntry]:

        return await self._store.retrieve(
            query=query,
            limit=limit,
            threshold=threshold,
            category=category,
        )