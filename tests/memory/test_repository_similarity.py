import pytest

from hios.db.models.memory_entry import MemoryRecord
from hios.db.repositories.memory_repository import MemoryRepository


@pytest.mark.asyncio
async def test_search_similar_returns_closest_memory(
    session,
):

    repository = MemoryRepository(
        session,
    )

    first = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
        embedding=[1.0] + [0.0] * 1535,
    )

    second = MemoryRecord(
        category="strategy",
        description="Check bathrooms after kitchens.",
        confidence=1.0,
        embedding=[0.0, 1.0] + [0.0] * 1534,
    )

    await repository.save(first)
    await repository.save(second)

    results = await repository.search_similar(
        embedding=[1.0] + [0.0] * 1535,
        limit=1,
    )

    assert len(results) == 1

    assert results[0].description == (
        "Inspect kitchens first."
    )
    