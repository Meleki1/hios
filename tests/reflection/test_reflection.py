import pytest

from hios.capabilities.reflection.default import (
    DefaultReflector,
)

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.goals.models.priority import GoalPriority


@pytest.fixture
def reflector():

    return DefaultReflector()


@pytest.fixture
def outcome():

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

    return Outcome(
        execution=execution,
        status=OutcomeStatus.SUCCESS,
    )


def test_returns_reflection(
    reflector,
    outcome,
):

    reflection = reflector.reflect(
        outcome,
    )

    assert reflection.outcome == outcome

def test_generates_insight(
    reflector,
    outcome,
):

    reflection = reflector.reflect(
        outcome,
    )

    assert len(reflection.insights) > 0


def test_success_generates_success_insight(
    reflector,
    outcome,
):

    reflection = reflector.reflect(
        outcome,
    )

    assert (
        reflection.insights[0].category
        == "success"
    )

def test_generates_summary(
    reflector,
    outcome,
):

    reflection = reflector.reflect(
        outcome,
    )

    assert reflection.summary != ""

def test_success_score_is_one(
    reflector,
    outcome,
):

    reflection = reflector.reflect(
        outcome,
    )

    assert reflection.score == 1.0

def test_failed_execution():

    reflector = DefaultReflector()

    plan = Plan(
        goal_id="goal",
        name="Plan",
        description="Description",
        priority=GoalPriority.CRITICAL,
    )

    decision = Decision(
        plan=plan,
        rationale="",
        score=1.0,
    )

    execution = Execution(
        decision=decision,
        status=ExecutionStatus.FAILED,
    )

    outcome = Outcome(
        execution=execution,
        status=OutcomeStatus.FAILED,
    )

    reflection = reflector.reflect(
        outcome,
    )

    assert (
        reflection.insights[0].category
        == "failure"
    )

    assert reflection.score == 0.0

