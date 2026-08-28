import pytest
from hios.db.models.memory_entry import MemoryRecord
from hios.db.models.memory_entry import MemoryRecord


def test_memory_record_accepts_embedding():

    embedding = [0.1] * 1536

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
        embedding=embedding,
    )

    assert record.embedding == embedding
    assert len(record.embedding) == 1536




@pytest.mark.asyncio
async def test_embedding_persists_to_database(
    session,
):
    embedding = [0.1] * 1536

    record = MemoryRecord(
        category="strategy",
        description="Inspect kitchens first.",
        confidence=1.0,
        embedding=embedding,
    )

    session.add(record)

    await session.commit()
    await session.refresh(record)

    assert record.embedding == embedding