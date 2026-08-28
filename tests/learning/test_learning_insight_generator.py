"""from hios.capabilities.learning.learning_insight_generator import (
    LearningInsightGenerator,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)




def test_learning_insight_generator_creates_signal_insight():

    generator = LearningInsightGenerator()

    pattern = LearningPattern(
        target="pest_control_need",
        sample_size=4,
        correct_count=3,
        incorrect_count=1,
        accuracy=0.75,
        lesson="Predictions were correct 75.0% of the time.",
        signal_performance={
            "asked_about_pests": SignalPerformance(
                sample_size=4,
                correct_count=3,
                incorrect_count=1,
                accuracy=0.75,
            ),
        },
    )

    insights = generator.generate(
        [pattern],
    )

    assert len(insights) == 1

    insight = insights[0]

    assert insight.target == (
        "pest_control_need"
    )

    assert insight.signal_name == (
        "asked_about_pests"
    )

    assert insight.sample_size == 4

    assert insight.accuracy == 0.75

    assert (
        "asked_about_pests"
        in insight.insight
    )

    assert (
        "75.0%"
        in insight.insight
    )
    assert insight.correct_count == 3
    assert insight.incorrect_count == 1

import pytest

from hios.capabilities.learning.insight_generator import (
    BasicLearningInsightGenerator,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)


def make_pattern() -> LearningPattern:
    return LearningPattern(
        target="pest_control_need",
        sample_size=5,
        correct_count=4,
        incorrect_count=1,
        accuracy=0.8,
        lesson=(
            "Predictions for pest_control_need "
            "were correct 80.0% of the time."
        ),
        signal_performance={
            "asked_about_pests": SignalPerformance(
                sample_size=5,
                correct_count=4,
                incorrect_count=1,
                accuracy=0.8,
            ),
            "repeat_visit": SignalPerformance(
                sample_size=3,
                correct_count=3,
                incorrect_count=0,
                accuracy=1.0,
            ),
        },
    )




   

@pytest.mark.asyncio
async def test_learning_insight_generator_creates_insights():

    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    insights = await generator.generate(
        pattern,
    )

    assert len(insights) == 2


@pytest.mark.asyncio
async def test_learning_insight_generator_preserves_target():

    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    insights = await generator.generate(
        pattern,
    )

    assert all(
        insight.target == "pest_control_need"
        for insight in insights
    )


@pytest.mark.asyncio
async def test_learning_insight_generator_creates_signal_insight():

    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    insights = await generator.generate(
        pattern,
    )

    insight = next(
        insight
        for insight in insights
        if insight.signal_name
        == "asked_about_pests"
    )

    assert insight.signal_name == (
        "asked_about_pests"
    )

    assert insight.sample_size == 5

    assert insight.accuracy == pytest.approx(
        0.8
    )


@pytest.mark.asyncio
async def test_learning_insight_generator_creates_repeat_visit_insight():

    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    insights = await generator.generate(
        pattern,
    )

    insight = next(
        insight
        for insight in insights
        if insight.signal_name
        == "repeat_visit"
    )

    assert insight.sample_size == 3

    assert insight.accuracy == pytest.approx(
        1.0
    )


@pytest.mark.asyncio
async def test_learning_insight_generator_creates_explanation():

    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    insights = await generator.generate(
        pattern,
    )

    insight = next(
        insight
        for insight in insights
        if insight.signal_name
        == "asked_about_pests"
    )

    assert insight.insight == (
        "The signal asked_about_pests was "
        "associated with pest_control_need "
        "being correct 80.0% of the time."
    )"""

import pytest

from hios.capabilities.learning.insight_generator import (
    BasicLearningInsightGenerator,
)
from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)


def make_pattern() -> LearningPattern:
    return LearningPattern(
        target="pest_control_need",
        sample_size=10,
        correct_count=8,
        incorrect_count=2,
        accuracy=0.8,
        lesson=(
            "Predictions for pest_control_need "
            "were correct 80.0% of the time."
        ),
        signal_performance={
            "asked_about_pests": SignalPerformance(
                sample_size=10,
                correct_count=8,
                incorrect_count=2,
                accuracy=0.8,
            ),
        },
    )


def test_learning_insight_generator_creates_insight():
    generator = BasicLearningInsightGenerator()

    pattern = make_pattern()

    result = generator.generate(
        [pattern],
    )

    assert len(result) == 1

    insight = result[0]

    assert isinstance(
        insight,
        LearningInsight,
    )

    assert insight.target == (
        "pest_control_need"
    )

    assert insight.signal_name == (
        "asked_about_pests"
    )

    assert insight.sample_size == 10
    assert insight.correct_count == 8
    assert insight.incorrect_count == 2
    assert insight.accuracy == 0.8

    assert insight.insight == (
        "The signal asked_about_pests "
        "was associated with pest_control_need "
        "being correct 80.0% of the time."
    )
def test_learning_insight_generator_creates_one_insight_per_signal():
    generator = BasicLearningInsightGenerator()

    pattern = LearningPattern(
        target="pest_control_need",
        sample_size=10,
        correct_count=8,
        incorrect_count=2,
        accuracy=0.8,
        lesson="Predictions were correct 80.0% of the time.",
        signal_performance={
            "asked_about_pests": SignalPerformance(
                sample_size=10,
                correct_count=8,
                incorrect_count=2,
                accuracy=0.8,
            ),
            "visited_service_page": SignalPerformance(
                sample_size=5,
                correct_count=4,
                incorrect_count=1,
                accuracy=0.8,
            ),
        },
    )

    result = generator.generate(
        [pattern],
    )

    assert len(result) == 2

    assert result[0].signal_name == (
        "asked_about_pests"
    )

    assert result[1].signal_name == (
        "visited_service_page"
    )