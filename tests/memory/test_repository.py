import pytest

from hios.db.models.memory_entry import MemoryRecord
from hios.db.repositories.memory_repository import MemoryRepository


@pytest.mark.asyncio
async def test_save_memory(
    session,
):

    repository = MemoryRepository(
        session,
    )

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
    )

    saved = await repository.save(
        record,
    )

    assert saved.id == record.id
    assert saved.category == "strategy"
    assert saved.description == "Inspect kitchens first."
    assert saved.confidence == 1.0


@pytest.mark.asyncio
async def test_retrieve_memory(
    session,
):

    repository = MemoryRepository(
        session,
    )

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
    )

    await repository.save(
        record,
    )

    results = await repository.retrieve(
        "kitchen",
    )


    assert len(results) == 1
    assert results[0].description == "Inspect kitchens first."


@pytest.mark.asyncio
async def test_retrieve_returns_empty_when_not_found(
    session,
):

    repository = MemoryRepository(
        session,
    )

    results = await repository.retrieve(
        "garage",
    )

    assert results == []


@pytest.mark.asyncio
async def test_list_memories(
    session,
):

    repository = MemoryRepository(
        session,
    )

    await repository.save(
        MemoryRecord(
            category="strategy",
            description="Inspect kitchens.",
        )
    )

    await repository.save(
        MemoryRecord(
            category="inspection",
            description="Inspect attic.",
        )
    )

    memories = await repository.list()

    assert len(memories) == 2


@pytest.mark.asyncio
async def test_delete_memory(
    session,
):

    repository = MemoryRepository(
        session,
    )

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens.",
    )

    await repository.save(
        record,
    )

    await repository.delete(
        record,
    )

    memories = await repository.list()

    assert memories == []


@pytest.mark.asyncio
async def test_saved_memory_persists_all_fields(
    session,
):

    repository = MemoryRepository(
        session,
    )

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=0.85,
        details={
            "source": "reflection",
        },
    )

    await repository.save(
        record,
    )

    retrieved = await repository.retrieve(
        "kitchen",
    )

    assert len(retrieved) == 1

    memory = retrieved[0]

    assert memory.category == "strategy"
    assert memory.description == "Inspect kitchens first."
    assert memory.confidence == 0.85
    assert memory.details["source"] == "reflection"

@pytest.mark.asyncio
async def test_save_generates_primary_key(
    session,
):

    repository = MemoryRepository(session)

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchen",
    )

    saved = await repository.save(record)

    assert saved.id is not None
    assert isinstance(saved.id, str)