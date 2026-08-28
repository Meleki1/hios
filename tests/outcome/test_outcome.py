from hios.capabilities.outcome.models.status import (
    OutcomeStatus,
)


def test_success():

    assert (
        OutcomeStatus.SUCCESS
        == "success"
    )


def test_partial():

    assert (
        OutcomeStatus.PARTIAL
        == "partial"
    )


def test_failed():

    assert (
        OutcomeStatus.FAILED
        == "failed"
    )


def test_unknown():

    assert (
        OutcomeStatus.UNKNOWN
        == "unknown"
    )


def test_all_statuses_are_unique():

    statuses = list(
        OutcomeStatus
    )

    assert len(statuses) == len(
        set(statuses)
    )

from hios.capabilities.outcome.models.observation import (
    OutcomeObservation,
)


def test_create_observation():

    observation = OutcomeObservation(
        action_id="inspect",
        description="Rodent droppings found.",
    )

    assert observation.action_id == "inspect"
    assert observation.description == "Rodent droppings found."


def test_serialization():

    observation = OutcomeObservation(
        action_id="inspect",
        description="Droppings found.",
    )

    dumped = observation.model_dump()

    assert dumped["action_id"] == "inspect"


def test_copy():

    observation = OutcomeObservation(
        action_id="inspect",
        description="Droppings found.",
    )

    copied = observation.model_copy()

    assert copied == observation

import pytest

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus
from hios.capabilities.outcome.models.observation import (
    OutcomeObservation,
)
from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus
from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.goals.models.priority import GoalPriority


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


def test_create_outcome(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    assert outcome.execution == execution


def test_default_status(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    assert outcome.status == OutcomeStatus.UNKNOWN


def test_default_observations(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    assert outcome.observations == []


def test_add_observations(
    execution,
):

    outcome = Outcome(
        execution=execution,
        observations=[
            OutcomeObservation(
                action_id="inspect",
                description="Droppings found.",
            )
        ],
    )

    assert len(outcome.observations) == 1


def test_default_summary(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    assert outcome.summary == ""


def test_serialization(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    dumped = outcome.model_dump()

    assert dumped["status"] == OutcomeStatus.UNKNOWN


def test_copy(
    execution,
):

    outcome = Outcome(
        execution=execution,
    )

    copied = outcome.model_copy()

    assert copied == outcome


def test_default_observations_are_independent(
    execution,
):

    outcome1 = Outcome(
        execution=execution,
    )

    outcome2 = Outcome(
        execution=execution,
    )

    outcome1.observations.append(
        OutcomeObservation(
            action_id="inspect",
            description="Found evidence.",
        )
    )

    assert outcome2.observations == []