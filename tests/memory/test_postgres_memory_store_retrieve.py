import pytest

from hios.capabilities.memory.postgres import (
    PostgresMemoryStore,
)
from hios.db.models.memory_entry import MemoryRecord
from uuid import uuid4

class FakeEmbedder:

    def __init__(self):
        self.texts: list[str] = []

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        self.texts.append(text)

        if text == "Where should I inspect first?":
            return [1.0] + [0.0] * 1535

        return [0.0] * 1536


class FakeRepository:

    def __init__(self):
        self.embedding = None
        self.limit = None
        self.threshold = None

    async def search_similar(
        self,
        embedding: list[float],
        limit: int = 5,
        threshold=0.70,
    ):
        self.embedding = embedding
        self.limit = limit
        self.threshold = threshold

        assert embedding == [1.0] + [0.0] * 1535

        return [
            MemoryRecord(
                id=str(uuid4()),
                category="strategy",
                description="Inspect kitchens first.",
                confidence=1.0,
                details={},
                embedding=[1.0] + [0.0] * 1535,
            )
        ]





@pytest.mark.asyncio
async def test_retrieve_uses_semantic_search():

    embedder = FakeEmbedder()
    repository = FakeRepository()

    store = PostgresMemoryStore(
        repository=repository,
        embedder=embedder,
    )

    results = await store.retrieve(
        "Where should I inspect first?",
    )

    assert embedder.texts == [
        "Where should I inspect first?",
    ]

    assert len(results) == 1

    assert results[0].description == (
        "Inspect kitchens first."
    )