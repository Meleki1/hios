import pytest
from sqlalchemy import delete

from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.postgres.learning_insight_repository import (
    PostgresLearningInsightRepository,
)
from hios.capabilities.learning.postgres.models.learning_insight_record import (
    LearningInsightModel,
)


def make_insight() -> LearningInsight:
    return LearningInsight(
        target="pest_control_need",
        signal_name="asked_about_pests",
        sample_size=10,
        correct_count=8,
        incorrect_count=2,
        accuracy=0.8,
        insight=(
            "The signal asked_about_pests "
            "was associated with pest_control_need "
            "being correct 80.0% of the time."
        ),
    )


@pytest.mark.asyncio
async def test_learning_insight_repository_saves_record(
    session,
):
    repository = PostgresLearningInsightRepository(
        session,
    )

    insight = make_insight()

    result = await repository.save(
        insight,
    )

    assert result.id == insight.id
    assert result.target == "pest_control_need"
    assert result.signal_name == "asked_about_pests"
    assert result.sample_size == 10
    assert result.correct_count == 8
    assert result.incorrect_count == 2
    assert result.accuracy == 0.8
    assert result.insight == insight.insight


@pytest.mark.asyncio
async def test_learning_insight_repository_gets_all(
    session,
):
    # Ensure this test starts with an empty table.
    await session.execute(
        delete(LearningInsightModel)
    )
    await session.commit()

    repository = PostgresLearningInsightRepository(
        session,
    )

    insight = make_insight()

    await repository.save(
        insight,
    )

    results = await repository.get_all()

    assert len(results) == 1

    result = results[0]

    assert result.id == insight.id
    assert result.target == "pest_control_need"
    assert result.signal_name == "asked_about_pests"
    assert result.sample_size == 10
    assert result.correct_count == 8
    assert result.incorrect_count == 2
    assert result.accuracy == 0.8
    assert result.insight == insight.insight