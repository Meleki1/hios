import pytest


from hios.capabilities.memory.service import MemoryService

class FakeMemoryFormation:

    def __init__(self):
        self.learning = None

        self.memories = [
            MemoryEntry(
                id="memory-1",
                category="strategy",
                description="Inspect kitchens first.",
                confidence=1.0,
                details={},
            )
        ]

    async def extract(self, learning):

        return []




class FakeMemoryStore:

    def __init__(self):
        self.learning = None
        self.query = None
        self.limit = None
        self.threshold = None
        self.category = None

    async def store(self, learning):
        self.learning = learning

        return [
            MemoryEntry(
                category="strategy",
                description="Inspect kitchens first.",
                confidence=1.0,
            )
        ]

    async def retrieve(
        self,
        query,
        limit=5,
        threshold=0.70,
        category=None,
    ):
        self.query = query
        self.limit = limit
        self.threshold = threshold
        self.category = category

        return [
            MemoryEntry(
                category="strategy",
                description="Inspect kitchens first.",
                confidence=1.0,
            )
        ]


@pytest.mark.asyncio
async def test_recall_delegates_to_memory_store():

    store = FakeMemoryStore()

    memory = MemoryService(
        store=store,
        formation=FakeMemoryFormation(),
    )

    results = await memory.recall(
        query="Where should I inspect first?",
        limit=3,
        threshold=0.80,
        category="strategy",
    )

    assert store.query == (
        "Where should I inspect first?"
    )

    assert store.limit == 3
    assert store.threshold == 0.80
    assert store.category == "strategy"

    assert len(results) == 1

    assert results[0].description == (
        "Inspect kitchens first."
    )

@pytest.mark.asyncio
async def test_remember_forms_memories_before_storing():

    store = FakeMemoryStore()
    formation = FakeMemoryFormation()

    service = MemoryService(
        store=store,
        formation=formation,
    )

    learning = object()

    results = await service.remember(
        learning,
    )

    assert formation.learning is learning
    assert store.memories is formation.memories

    assert len(results) == 1

    assert results[0].description == (
        "Inspect kitchens first."
    )