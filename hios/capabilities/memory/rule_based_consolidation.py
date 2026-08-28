from hios.capabilities.memory.consolidation import (
    MemoryConsolidator,
)
from hios.capabilities.memory.models.memory_entry import MemoryEntry


class RuleBasedMemoryConsolidator(MemoryConsolidator):

    async def consolidate(
        self,
        memories: list[MemoryEntry],
    ) -> MemoryEntry:

        if not memories:
            raise ValueError(
                "Cannot consolidate empty memories."
            )

        if len(memories) == 1:
            return memories[0]

        primary = memories[0]

        descriptions = [
            memory.description.strip()
            for memory in memories
            if memory.description.strip()
        ]

        description = " ".join(descriptions)

        confidence = max(
            memory.confidence
            for memory in memories
        )

        return MemoryEntry(
            id=primary.id,
            category=primary.category,
            description=description,
            confidence=confidence,
        )