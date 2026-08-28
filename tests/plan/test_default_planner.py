import pytest

from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.default_planner import DefaultPlanner
from hios.capabilities.planning.models.plan import Plan

@pytest.fixture
def planner():

    return DefaultPlanner()

@pytest.fixture
def priority():
    return GoalPriority.CRITICAL


@pytest.fixture
def eliminate_goal():

    return Goal(
        id="eliminate_infestation",
        name="Eliminate infestation",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )


@pytest.fixture
def prevent_goal():

    return Goal(
        id="prevent_recurrence",
        name="Prevent recurrence",
        description="Prevent rodents returning.",
        priority=GoalPriority.HIGH,
    )

def test_empty_goals_return_no_plans(planner):

    result = GoalResult()

    plans = planner.create(result)

    assert plans == []

def test_eliminate_goal_generates_plan(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    assert len(plans) == 1

    assert plans[0].goal_id == eliminate_goal.id

def test_plan_contains_tasks(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    assert len(plans[0].tasks) == 4

def test_task_order(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    names = [
        task.name
        for task in plans[0].tasks
    ]

    assert names == [
        "Inspect property",
        "Seal entry points",
        "Deploy traps",
        "Schedule follow-up",
    ]

def test_constraints(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    assert len(plans[0].constraints) == 1

    assert plans[0].constraints[0].name == "Safety"

def test_multiple_goals(
    planner,
    eliminate_goal,
    prevent_goal,
):

    result = GoalResult(
        goals=[
            eliminate_goal,
            prevent_goal,
        ]
    )

    plans = planner.create(result)

    assert len(plans) == 2

def test_duplicate_goals(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[
            eliminate_goal,
            eliminate_goal,
        ]
    )

    plans = planner.create(result)

    ids = [
        plan.goal_id
        for plan in plans
    ]

    assert len(ids) == len(set(ids))

def test_unknown_goal_returns_no_plan(
    planner,
):

    result = GoalResult(
        goals=[
            Goal(
                id="unknown",
                name="Unknown Goal",
                description="...",
                priority=GoalPriority.MEDIUM,
            )
        ]
    )

    plans = planner.create(result)

    assert plans == []

def test_priority_preserved(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    assert plans[0].priority == GoalPriority.CRITICAL

def test_generated_plan_has_id(
    planner,
    eliminate_goal,
):

    result = GoalResult(
        goals=[eliminate_goal],
    )

    plans = planner.create(result)

    assert plans[0].id != ""

def test_planner_creates_visual_evidence_task():
    goal = Goal(
        id="goal-1",
        name="Gather visual evidence",
        description=(
            "Obtain visual evidence to better understand "
            "the suspected pest activity."
        ),
       
    )

    plans = DefaultPlanner().create(
        GoalResult(goals=[goal])
    )

    assert plans

    plan = plans[0]

    assert plan.tasks

    task = plan.tasks[0]

    assert task.required is True
    assert "image" in task.name.lower()
    

def test_planner_visual_evidence_task_explains_why_image_is_needed():
    goal = Goal(
        id="goal-1",
        name="Gather visual evidence",
        description=(
            "Obtain visual evidence to identify "
            "the suspected pest."
        ),
        priority=GoalPriority.HIGH,
    )

    plans = DefaultPlanner().create(
        GoalResult(goals=[goal])
    )

    assert plans

    task = plans[0].tasks[0]

    assert "evidence" in task.description.lower()

def test_planner_does_not_request_image_for_normal_goal():
    goal = Goal(
        id="goal-1",
        name="Prevent recurrence",
        description="Reduce the likelihood of future infestations.",
        priority=GoalPriority.HIGH,
    )

    plans = DefaultPlanner().create(
        GoalResult(goals=[goal])
    )

    assert plans
    assert all(
        "image" not in task.name.lower()
        for plan in plans
        for task in plan.tasks
    )