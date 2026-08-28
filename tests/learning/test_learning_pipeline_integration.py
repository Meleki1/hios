import pytest
from sqlalchemy import delete

from hios.capabilities.learning.basic_learning_analyzer import (
    BasicLearningAnalyzer,
)
from hios.capabilities.learning.insight_generator import (
    BasicLearningInsightGenerator,
)
from hios.capabilities.learning.learning_pipeline import (
    LearningPipeline,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.postgres.learning_insight_repository import (
    PostgresLearningInsightRepository,
)
from hios.capabilities.learning.postgres.models.learning_insight_record import (
    LearningInsightModel,
)
from hios.capabilities.learning.learning_insight_generator import (
    LearningInsightGenerator,
)

def make_learning_record(
    *,
    correct: bool,
) -> LearningRecord:
    return LearningRecord(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        evaluation_id="evaluation-1",
        target="pest_control_need",
        correct=correct,
        signal_names=[
            "asked_about_pests",
        ],
        signal_values=[
            "pest_control",
        ],
        signal_strengths=[
            1.0,
        ],
        signal_confidences=[
            1.0,
        ],
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson=(
            "Prediction was correct."
            if correct
            else "Prediction was incorrect."
        ),
    )
    
def make_record(
    prediction_id: str,
    correct: bool,
) -> LearningRecord:

    return LearningRecord(
        prediction_id=prediction_id,
        outcome_id=f"outcome-{prediction_id}",
        evaluation_id=f"evaluation-{prediction_id}",
        target="pest_control_need",
        correct=correct,
        signal_names=["asked_about_pests"],
        signal_values=["pest_control"],
        signal_strengths=[1.0],
        signal_confidences=[0.9],
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson=(
            "Prediction was correct."
            if correct
            else "Prediction was incorrect."
        ),
    )


@pytest.mark.asyncio
async def test_learning_pipeline_persists_insight(
    session,
):

    await session.execute(
        delete(LearningInsightModel)
    )
    await session.commit()

    analyzer = BasicLearningAnalyzer()

    generator = BasicLearningInsightGenerator()

    repository = PostgresLearningInsightRepository(
        session,
    )

    pipeline = LearningPipeline(
        analyzer=analyzer,
        insight_generator=generator,
        insight_repository=repository,
    )

    records = [
        make_record("prediction-1", True),
        make_record("prediction-2", True),
        make_record("prediction-3", False),
        make_record("prediction-4", True),
        make_record("prediction-5", True),
    ]

    result = await pipeline.process(
        records,
    )

    assert len(result) == 1

    insight = result[0]

    assert insight.target == (
        "pest_control_need"
    )

    assert insight.signal_name == (
        "asked_about_pests"
    )

    assert insight.sample_size == 5

    assert insight.correct_count == 4

    assert insight.incorrect_count == 1

    assert insight.accuracy == 0.8

    stored = await repository.get_all()

    assert len(stored) == 1

    assert stored[0].id == insight.id
    assert stored[0].target == insight.target
    assert stored[0].signal_name == insight.signal_name
    assert stored[0].sample_size == 5
    assert stored[0].correct_count == 4
    assert stored[0].incorrect_count == 1
    assert stored[0].accuracy == 0.8


@pytest.mark.asyncio
async def test_learning_insight_flow():
    analyzer = BasicLearningAnalyzer()
    generator = LearningInsightGenerator()

    records = [
        make_learning_record(correct=True),
        make_learning_record(correct=True),
        make_learning_record(correct=False),
    ]

    patterns = await analyzer.analyze(records)

    insights = generator.generate(patterns)

    assert len(patterns) == 1
    assert patterns[0].sample_size == 3
    assert patterns[0].correct_count == 2
    assert patterns[0].incorrect_count == 1
    assert patterns[0].accuracy == pytest.approx(2 / 3)

    assert len(insights) == 1

    insight = insights[0]

    assert insight.target == "pest_control_need"
    assert insight.signal_name == "asked_about_pests"
    assert insight.sample_size == 3
    assert insight.correct_count == 2
    assert insight.incorrect_count == 1
    assert insight.accuracy == pytest.approx(2 / 3)