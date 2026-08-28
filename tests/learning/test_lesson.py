from hios.capabilities.learning.models.lesson import (
    Lesson,
)


def test_create_lesson():

    lesson = Lesson(
        category="strategy",
        description="Inspect kitchens first.",
    )

    assert lesson.category == "strategy"
    assert lesson.description == "Inspect kitchens first."


def test_default_confidence():

    lesson = Lesson(
        category="strategy",
        description="Inspect kitchens first.",
    )

    assert lesson.confidence == 1.0


def test_serialization():

    lesson = Lesson(
        category="strategy",
        description="Inspect kitchens first.",
    )

    dumped = lesson.model_dump()

    assert dumped["category"] == "strategy"


def test_copy():

    lesson = Lesson(
        category="strategy",
        description="Inspect kitchens first.",
    )

    copied = lesson.model_copy()

    assert copied == lesson


def test_unique_ids():

    lesson1 = Lesson(
        category="strategy",
        description="A",
    )

    lesson2 = Lesson(
        category="strategy",
        description="B",
    )

    assert lesson1.id != lesson2.id