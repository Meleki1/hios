import pytest

from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.rule_based_consolidation import (
    RuleBasedMemoryConsolidator,
)


@pytest.mark.asyncio
async def test_consolidates_memories():

    consolidator = RuleBasedMemoryConsolidator()

    memories = [
        MemoryEntry(
            id="1",
            category="strategy",
            description="Inspect kitchens first.",
            confidence=0.8,
        ),
        MemoryEntry(
            id="2",
            category="strategy",
            description="Start with the kitchen.",
            confidence=0.9,
        ),
    ]

    result = await consolidator.consolidate(
        memories,
    )

    assert result.id == "1"

    assert result.category == "strategy"

    assert result.description == (
        "Inspect kitchens first. Start with the kitchen."
    )

    assert result.confidence == 0.9