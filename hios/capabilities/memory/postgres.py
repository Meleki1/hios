from hios.capabilities.learning.models.lesson import Lesson
from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.store import MemoryStore
from hios.db.models.memory_entry import MemoryRecord
from hios.db.repositories.memory_repository import MemoryRepository
from hios.capabilities.memory.embedding import OpenAIEmbedder

class PostgresMemoryStore(MemoryStore):

    def __init__(
        self,
        repository: MemoryRepository,
        embedder: OpenAIEmbedder
    ):
        self._repository = repository
        self._embedder = embedder

    async def store(
        self,
        memories: list[MemoryEntry],
    ) -> list[MemoryEntry]:

        for memory in memories:

            embedding = await self._embedder.embed(
                memory.description,
            )

            record = MemoryRecord(
                id=memory.id,
                category=memory.category,
                description=memory.description,
                confidence=memory.confidence,
                details=memory.details,
                embedding=embedding,
            )

            await self._repository.save(record)

        return memories

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.70,
        category: str | None = None,
    ) -> list[MemoryEntry]:

        embedding = await self._embedder.embed(query)

        records = await self._repository.search_similar(
            embedding=embedding,
            limit=limit,
            threshold=threshold,
            category=category,
        )

        return [
            MemoryEntry(
                id=record.id,
                category=record.category,
                description=record.description,
                confidence=record.confidence,
                details=record.details,
            )
            for record in records
        ]

    def _to_memory(
        self,
        lesson: Lesson,
    ) -> MemoryEntry:

        return MemoryEntry(
            id=lesson.id,
            category=lesson.category,
            description=lesson.description,
            confidence=lesson.confidence,
        )

    def _to_record(
        self,
        memory: MemoryEntry,
    ) -> MemoryRecord:

        return MemoryRecord(
            id=memory.id,
            category=memory.category,
            description=memory.description,
            confidence=memory.confidence,
            details=memory.details,
        )

    def _to_entry(
        self,
        record: MemoryRecord,
    ) -> MemoryEntry:

        return MemoryEntry(
            id=record.id,
            category=record.category,
            description=record.description,
            confidence=record.confidence,
            details=record.details,
        )
