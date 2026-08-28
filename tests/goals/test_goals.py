import pytest

from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.goals.models.status import GoalStatus


def test_create_goal():

    goal = Goal(
        name="Eliminate infestation",
        description="Remove the rodent infestation.",
    )

    assert goal.name == "Eliminate infestation"
    assert goal.description == "Remove the rodent infestation."


def test_goal_generates_unique_id():

    goal1 = Goal(
        name="Goal A",
        description="A",
    )

    goal2 = Goal(
        name="Goal B",
        description="B",
    )

    assert goal1.id != goal2.id


def test_default_priority():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    assert goal.priority == GoalPriority.MEDIUM


def test_default_status():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    assert goal.status == GoalStatus.PENDING


def test_custom_priority():

    goal = Goal(
        name="Goal",
        description="Description",
        priority=GoalPriority.CRITICAL,
    )

    assert goal.priority == GoalPriority.CRITICAL


def test_custom_status():

    goal = Goal(
        name="Goal",
        description="Description",
        status=GoalStatus.ACTIVE,
    )

    assert goal.status == GoalStatus.ACTIVE


def test_source_hypothesis():

    goal = Goal(
        name="Goal",
        description="Description",
        source_hypothesis="rodent",
    )

    assert goal.source_hypothesis == "rodent"


def test_goal_is_serializable():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    data = goal.model_dump()

    assert data["name"] == "Goal"
    assert data["description"] == "Description"


def test_goal_copy():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    copied = goal.model_copy()

    assert copied == goal
    assert copied is not goal


def test_goal_equality():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    copied = goal.model_copy()

    assert copied == goal


def test_goal_accepts_none_source_hypothesis():

    goal = Goal(
        name="Goal",
        description="Description",
    )

    assert goal.source_hypothesis is None


def test_goal_priority_enum():

    assert GoalPriority.LOW.value == "low"
    assert GoalPriority.MEDIUM.value == "medium"
    assert GoalPriority.HIGH.value == "high"
    assert GoalPriority.CRITICAL.value == "critical"


def test_goal_status_enum():

    assert GoalStatus.PENDING.value == "pending"
    assert GoalStatus.ACTIVE.value == "active"
    assert GoalStatus.COMPLETED.value == "completed"
    assert GoalStatus.FAILED.value == "failed"