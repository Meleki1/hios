import pytest

from hios.capabilities.memory.embedding import OpenAIEmbedder
from hios.core.config import get_settings
from hios.db.models.memory_entry import MemoryRecord
from hios.db.repositories.memory_repository import MemoryRepository
from uuid import uuid4


class FakeRepository:

    def __init__(self):
        self.embedding = None
        self.limit = None
        self.threshold = None

    async def search_similar(
        self,
        embedding,
        limit=5,
        threshold=0.70,
    ):

        self.embedding = embedding
        self.limit = limit
        self.threshold = threshold

        return []

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_semantic_retrieval(session):

    settings = get_settings()

    embedder = OpenAIEmbedder(
        api_key=settings.openai_api_key,
    )

    repository = MemoryRepository(
        session,
    )

    memory_embedding = await embedder.embed(
        "Inspect kitchens first.",
    )

    record = MemoryRecord(
        id=str(uuid4()),
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
        details={},
        embedding=memory_embedding,
    )

    await repository.save(record)

    query_embedding = await embedder.embed(
        "Where should I inspect first?",
    )

    results = await repository.search_similar(
        query_embedding,
        limit=1,
    )

    assert len(results) == 1

    assert results[0].description == (
        "Inspect kitchens first."
    )