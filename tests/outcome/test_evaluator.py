import pytest

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision

from hios.capabilities.goals.models.priority import GoalPriority

from hios.capabilities.planning.models.plan import Plan

from hios.capabilities.outcome.default import DefaultOutcomeEvaluator

from hios.capabilities.outcome.models.status import (
    OutcomeStatus,
)


@pytest.fixture
def evaluator():

    return DefaultOutcomeEvaluator()


@pytest.fixture
def execution():

    plan = Plan(
        goal_id="goal-1",
        name="Rodent Plan",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )

    decision = Decision(
        plan=plan,
        rationale="Highest priority.",
        score=1.0,
    )

    return Execution(
        decision=decision,
        status=ExecutionStatus.SUCCESS,
    )


def test_returns_outcome(
    evaluator,
    execution,
):

    outcome = evaluator.evaluate(
        execution,
    )

    assert outcome.execution == execution

def test_success_execution_returns_success(
    evaluator,
    execution,
):

    outcome = evaluator.evaluate(
        execution,
    )

    assert (
        outcome.status
        == OutcomeStatus.SUCCESS
    )

def test_failed_execution_returns_failed():

    evaluator = DefaultOutcomeEvaluator()

    plan = Plan(
        goal_id="goal-1",
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

    outcome = evaluator.evaluate(
        execution,
    )

    assert (
        outcome.status
        == OutcomeStatus.FAILED
    )

def test_pending_execution_returns_unknown():

    evaluator = DefaultOutcomeEvaluator()

    plan = Plan(
        goal_id="goal-1",
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
        status=ExecutionStatus.PENDING,
    )

    outcome = evaluator.evaluate(
        execution,
    )

    assert (
        outcome.status
        == OutcomeStatus.UNKNOWN
    )

def test_observations_default_empty(
    evaluator,
    execution,
):

    outcome = evaluator.evaluate(
        execution,
    )

    assert outcome.observations == []

def test_summary_default_empty(
    evaluator,
    execution,
):

    outcome = evaluator.evaluate(
        execution,
    )

    assert outcome.summary == ""