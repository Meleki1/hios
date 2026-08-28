from hios.capabilities.reflection.models.insight import (
    Insight,
)


def test_create_insight():

    insight = Insight(
        category="success",
        description="Inspection completed successfully.",
    )

    assert insight.category == "success"
    assert insight.description == (
        "Inspection completed successfully."
    )


def test_default_score():

    insight = Insight(
        category="success",
        description="Completed.",
    )

    assert insight.score == 1.0


def test_serialization():

    insight = Insight(
        category="risk",
        description="Rodent activity remains.",
    )

    dumped = insight.model_dump()

    assert dumped["category"] == "risk"


def test_copy():

    insight = Insight(
        category="risk",
        description="Rodent activity remains.",
    )

    copied = insight.model_copy()

    assert copied == insight


def test_unique_id():

    insight1 = Insight(
        category="risk",
        description="A",
    )

    insight2 = Insight(
        category="risk",
        description="B",
    )

    assert insight1.id != insight2.id