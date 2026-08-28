import pytest

from hios.capabilities.learning.default import DefaultLearner
from hios.capabilities.learning.models.lesson import Lesson

from hios.capabilities.reflection.models.reflection import Reflection
from hios.capabilities.reflection.models.insight import Insight

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.goals.models.priority import GoalPriority


@pytest.fixture
def learner():

    return DefaultLearner()


@pytest.fixture
def reflection():

    plan = Plan(
        goal_id="goal-1",
        name="Rodent Removal",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )

    decision = Decision(
        plan=plan,
        rationale="Highest priority.",
        score=1.0,
    )

    execution = Execution(
        decision=decision,
        status=ExecutionStatus.SUCCESS,
    )

    outcome = Outcome(
        execution=execution,
        status=OutcomeStatus.SUCCESS,
    )

    return Reflection(
        outcome=outcome,
        insights=[
            Insight(
                category="success",
                description="Inspection completed successfully.",
            )
        ],
        summary="Execution successful.",
        score=1.0,
    )

def test_returns_learning(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert learning.reflection == reflection

def test_generates_lesson(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert len(learning.lessons) == 1

def test_lesson_category_matches_insight(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert (
        learning.lessons[0].category
        == "success"
    )

def test_lesson_description_matches_insight(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert (
        learning.lessons[0].description
        == "Inspection completed successfully."
    )

def test_summary_copied(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert learning.summary == reflection.summary

def test_score_copied(
    learner,
    reflection,
):

    learning = learner.learn(
        reflection,
    )

    assert learning.score == reflection.score

def test_empty_reflection():

    learner = DefaultLearner()

    reflection = Reflection(
        outcome=Outcome(
            execution=Execution(
                decision=Decision(
                    plan=Plan(
                        goal_id="1",
                        name="Plan",
                        description="Description",
                        priority=GoalPriority.CRITICAL,
                    ),
                    rationale="",
                    score=1.0,
                ),
                status=ExecutionStatus.SUCCESS,
            ),
            status=OutcomeStatus.SUCCESS,
        ),
    )

    learning = learner.learn(
        reflection,
    )

    assert learning.lessons == []