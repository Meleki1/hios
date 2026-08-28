from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.goals.models.goal import Goal


def test_empty_goal_result():

    result = GoalResult()

    assert result.goals == []


def test_single_goal():

    result = GoalResult(
        goals=[
            Goal(
                name="Goal",
                description="Description",
            )
        ]
    )

    assert len(result.goals) == 1


def test_multiple_goals():

    result = GoalResult(
        goals=[
            Goal(
                name="Goal A",
                description="A",
            ),
            Goal(
                name="Goal B",
                description="B",
            ),
        ]
    )

    assert len(result.goals) == 2


def test_goal_order_preserved():

    result = GoalResult(
        goals=[
            Goal(
                name="First",
                description="A",
            ),
            Goal(
                name="Second",
                description="B",
            ),
        ]
    )

    assert result.goals[0].name == "First"
    assert result.goals[1].name == "Second"


def test_goal_result_serialization():

    result = GoalResult(
        goals=[
            Goal(
                name="Goal",
                description="Description",
            )
        ]
    )

    dumped = result.model_dump()

    assert len(dumped["goals"]) == 1