from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.formation import MemoryFormation


class RuleBasedMemoryFormation(MemoryFormation):

    async def extract(
        self,
        learning: Learning,
    ) -> list[MemoryEntry]:

        memories: list[MemoryEntry] = []

        for lesson in learning.lessons:

            if not lesson.description.strip():
                continue

            if lesson.confidence <= 0:
                continue

            memories.append(
                MemoryEntry(
                    id=lesson.id,
                    category=lesson.category,
                    description=lesson.description,
                    confidence=lesson.confidence,
                )
            )

        return memories