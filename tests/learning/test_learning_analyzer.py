"""import pytest

from hios.capabilities.learning.basic_learning_analyzer import (
    BasicLearningAnalyzer,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


def make_record(
    prediction_id: str,
    target: str,
    correct: bool,
    signal_names: list[str] | None = None,
) -> LearningRecord:

    return LearningRecord(
        prediction_id=prediction_id,
        outcome_id=f"outcome-{prediction_id}",
        evaluation_id=f"evaluation-{prediction_id}",
        target=target,
        correct=correct,
        signal_names=(
            signal_names
            if signal_names is not None
            else ["asked_about_pests"]
        ),
        signal_values=[
            "true",
        ],
        signal_strengths=[
            1.0,
        ],
        signal_confidences=[
            1.0,
        ],
        intent_score=70.0,
        prediction_confidence=1.0,
        lesson="",
    )


@pytest.mark.asyncio
async def test_learning_analyzer_calculates_accuracy():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            "prediction-1",
            "pest_control_need",
            True,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-2",
            "pest_control_need",
            False,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
    ]

    patterns = await analyzer.analyze(
        records,
    )

    assert len(patterns) == 1
    assert patterns[0].accuracy == pytest.approx(0.5)


@pytest.mark.asyncio
async def test_learning_analyzer_groups_by_target():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            "prediction-1",
            "pest_control_need",
            True,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-2",
            "pest_control_need",
            False,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-3",
            "damp_problem",
            True,
            signal_names=[
                "damp_signal",
            ],
        ),
    ]

    patterns = await analyzer.analyze(
        records,
    )

    assert len(patterns) == 2

    pest_pattern = next(
        pattern
        for pattern in patterns
        if pattern.target
        == "pest_control_need"
    )

    damp_pattern = next(
        pattern
        for pattern in patterns
        if pattern.target
        == "damp_problem"
    )

    assert pest_pattern.sample_size == 2
    assert pest_pattern.accuracy == pytest.approx(
        0.5
    )

    assert damp_pattern.sample_size == 1
    assert damp_pattern.accuracy == pytest.approx(
        1.0
    )

@pytest.mark.asyncio
async def test_learning_analyzer_groups_by_target():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            "prediction-1",
            "pest_control_need",
            True,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-2",
            "pest_control_need",
            False,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-3",
            "damp_problem",
            True,
            signal_names=[
                "damp_signal",
            ],
        ),
    ]

    patterns = await analyzer.analyze(
        records,
    )

    assert len(patterns) == 2

    pest_pattern = next(
        pattern
        for pattern in patterns
        if pattern.target
        == "pest_control_need"
    )

    damp_pattern = next(
        pattern
        for pattern in patterns
        if pattern.target
        == "damp_problem"
    )

    assert pest_pattern.sample_size == 2
    assert pest_pattern.accuracy == pytest.approx(
        0.5
    )

    assert damp_pattern.sample_size == 1
    assert damp_pattern.accuracy == pytest.approx(
        1.0
    )

@pytest.mark.asyncio
async def test_learning_analyzer_identifies_signal_performance():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            "prediction-1",
            "pest_control_need",
            True,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-2",
            "pest_control_need",
            False,
            signal_names=[
                "asked_about_pests",
                "repeat_visit",
            ],
        ),
        make_record(
            "prediction-3",
            "damp_problem",
            True,
            signal_names=[
                "damp_signal",
            ],
        ),
    ]

    patterns = await analyzer.analyze(
        records,
    )

    pattern = next(
        pattern
        for pattern in patterns
        if pattern.target == "pest_control_need"
    )

    asked_about_pests = (
        pattern.signal_performance[
            "asked_about_pests"
        ]
    )

    assert asked_about_pests.sample_size == 2
    assert asked_about_pests.correct_count == 1
    assert asked_about_pests.incorrect_count == 1
    assert asked_about_pests.accuracy == pytest.approx(0.5)

    repeat_visit = (
        pattern.signal_performance[
            "repeat_visit"
        ]
    )

    assert repeat_visit.sample_size == 2
    assert repeat_visit.correct_count == 1
    assert repeat_visit.incorrect_count == 1
    assert repeat_visit.accuracy == pytest.approx(0.5)"""

import pytest

from hios.capabilities.learning.basic_learning_analyzer import (
    BasicLearningAnalyzer,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


def make_record(
    *,
    prediction_id: str,
    target: str,
    correct: bool,
    signal_names: list[str],
) -> LearningRecord:
    return LearningRecord(
        prediction_id=prediction_id,
        outcome_id=f"outcome-{prediction_id}",
        evaluation_id=f"evaluation-{prediction_id}",
        target=target,
        correct=correct,
        signal_names=signal_names,
        signal_values=["pest_control"] * len(signal_names),
        signal_strengths=[1.0] * len(signal_names),
        signal_confidences=[1.0] * len(signal_names),
        intent_score=70.0,
        prediction_confidence=0.9,
        lesson="Prediction was correct.",
    )


@pytest.mark.asyncio
async def test_basic_learning_analyzer_builds_target_pattern():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            prediction_id="prediction-1",
            target="pest_control_need",
            correct=True,
            signal_names=["asked_about_pests"],
        ),
        make_record(
            prediction_id="prediction-2",
            target="pest_control_need",
            correct=True,
            signal_names=["asked_about_pests"],
        ),
        make_record(
            prediction_id="prediction-3",
            target="pest_control_need",
            correct=False,
            signal_names=["asked_about_pests"],
        ),
    ]

    patterns = await analyzer.analyze(records)

    assert len(patterns) == 1

    pattern = patterns[0]

    assert pattern.target == "pest_control_need"
    assert pattern.sample_size == 3
    assert pattern.correct_count == 2
    assert pattern.incorrect_count == 1
    assert pattern.accuracy == pytest.approx(2 / 3)

    assert pattern.lesson == (
        "Predictions for pest_control_need "
        "were correct 66.7% of the time."
    )


@pytest.mark.asyncio
async def test_basic_learning_analyzer_calculates_signal_performance():

    analyzer = BasicLearningAnalyzer()

    records = [
        make_record(
            prediction_id="prediction-1",
            target="pest_control_need",
            correct=True,
            signal_names=[
                "asked_about_pests",
                "requested_treatment",
            ],
        ),
        make_record(
            prediction_id="prediction-2",
            target="pest_control_need",
            correct=True,
            signal_names=[
                "asked_about_pests",
            ],
        ),
        make_record(
            prediction_id="prediction-3",
            target="pest_control_need",
            correct=False,
            signal_names=[
                "asked_about_pests",
                "requested_treatment",
            ],
        ),
    ]

    patterns = await analyzer.analyze(records)

    assert len(patterns) == 1

    pattern = patterns[0]

    asked_about_pests = pattern.signal_performance[
        "asked_about_pests"
    ]

    assert asked_about_pests.sample_size == 3
    assert asked_about_pests.correct_count == 2
    assert asked_about_pests.incorrect_count == 1
    assert asked_about_pests.accuracy == pytest.approx(2 / 3)

    requested_treatment = pattern.signal_performance[
        "requested_treatment"
    ]

    assert requested_treatment.sample_size == 2
    assert requested_treatment.correct_count == 1
    assert requested_treatment.incorrect_count == 1
    assert requested_treatment.accuracy == 0.5