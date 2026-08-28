import pytest

from hios.capabilities.memory.rule_based_formation import (
    RuleBasedMemoryFormation,
)


class FakeLesson:

    def __init__(
        self,
        id: str,
        category: str,
        description: str,
        confidence: float,
    ):
        self.id = id
        self.category = category
        self.description = description
        self.confidence = confidence


class FakeLearning:

    def __init__(self, lessons):
        self.lessons = lessons


@pytest.mark.asyncio
async def test_extracts_valid_lessons():

    formation = RuleBasedMemoryFormation()

    learning = FakeLearning(
        lessons=[
            FakeLesson(
                id="1",
                category="strategy",
                description="Inspect kitchens first.",
                confidence=1.0,
            ),
            FakeLesson(
                id="2",
                category="observation",
                description="",
                confidence=1.0,
            ),
            FakeLesson(
                id="3",
                category="strategy",
                description="Ignore this.",
                confidence=0.0,
            ),
        ],
    )

    memories = await formation.extract(
        learning,
    )

    assert len(memories) == 1

    assert memories[0].id == "1"

    assert memories[0].description == (
        "Inspect kitchens first."
    )

    assert memories[0].category == "strategy"