from hios.capabilities.memory.deduplication import (
    MemoryDeduplicator,
)
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.db.repositories.memory_repository import MemoryRepository


class PostgresMemoryDeduplicator(MemoryDeduplicator):

    def __init__(
        self,
        repository: MemoryRepository,
        embedder,
        threshold: float = 0.90,
    ):
        self._repository = repository
        self._embedder = embedder
        self._threshold = threshold

    async def is_duplicate(
        self,
        memory: MemoryEntry,
    ) -> bool:

        embedding = await self._embedder.embed(
            memory.description,
        )

        results = await self._repository.search_similar(
            embedding=embedding,
            limit=1,
            threshold=self._threshold,
        )

        return len(results) > 0