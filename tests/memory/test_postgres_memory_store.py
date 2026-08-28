import pytest
from uuid import uuid4
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.postgres import PostgresMemoryStore
from hios.db.models.memory_entry import MemoryRecord


class FakeEmbedder:

    def __init__(self):
        self.texts: list[str] = []

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        self.texts.append(text)

        return [0.1] * 1536


class FakeRepository:

    def __init__(self):
        self.records: list[MemoryRecord] = []

    async def save(
        self,
        record: MemoryRecord,
    ) -> MemoryRecord:

        self.records.append(record)

        return record


class FakeLesson:

    def __init__(
        self,
        category: str,
        description: str,
        confidence: float,
    ):
        self.id = str(uuid4())
        self.category = category
        self.description = description
        self.confidence = confidence


class FakeLearning:

    def __init__(
        self,
        lessons,
    ):
        self.lessons = lessons


@pytest.mark.asyncio
async def test_store_generates_and_persists_embedding():

    embedder = FakeEmbedder()
    repository = FakeRepository()

    store = PostgresMemoryStore(
        repository=repository,
        embedder=embedder,
    )

    memory = MemoryEntry(
        id="memory-1",
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
        details={},
    )

    result = await store.store(
        [memory],
    )

    assert result[0].description == "Inspect kitchens first."