import pytest

from hios.capabilities.planning.models.task import Task
from hios.capabilities.goals.models.priority import GoalPriority


def test_create_task():

    task = Task(
        name="Inspect property",
        description="Inspect the affected property.",
    )

    assert task.name == "Inspect property"
    assert task.description == "Inspect the affected property."


def test_task_generates_unique_id():

    task1 = Task(
        name="Task A",
        description="A",
        
    )

    task2 = Task(
        name="Task B",
        description="B",
    )

    assert task1.id != task2.id


def test_required_defaults_true():

    task = Task(
        name="Inspect",
        description="Inspect property.",
        
    )

    assert task.required is True


def test_required_can_be_false():

    task = Task(
        name="Optional Survey",
        description="Survey neighboring property.",
        required=False,
    )

    assert task.required is False


def test_task_serialization():

    task = Task(
        name="Inspect",
        description="Inspect property.",
    )

    data = task.model_dump()

    assert data["name"] == "Inspect"


def test_task_copy():

    task = Task(
        name="Inspect",
        description="Inspect property.",
    )

    copied = task.model_copy()

    assert copied == task
    assert copied is not task


def test_task_equality():

    task = Task(
        name="Inspect",
        description="Inspect property.",
    )

    copied = task.model_copy()

    assert copied == task

from hios.capabilities.planning.models.constraint import Constraint


def test_create_constraint():

    constraint = Constraint(
        name="Safety",
        description="Wear protective equipment.",
    )

    assert constraint.name == "Safety"
    assert constraint.description == "Wear protective equipment."


def test_constraint_serialization():

    constraint = Constraint(
        name="Budget",
        description="Do not exceed allocated budget.",
        
    )

    data = constraint.model_dump()

    assert data["name"] == "Budget"


def test_constraint_copy():

    constraint = Constraint(
        name="Time",
        description="Complete within 24 hours.",
        
    )

    copied = constraint.model_copy()

    assert copied == constraint


from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.models.task import Task
from hios.capabilities.planning.models.constraint import Constraint


def test_create_plan():

    plan = Plan(
        goal_id="goal-1",
        name="Rodent Removal Plan",
        description="Plan to eliminate rodents.",
        priority=GoalPriority.HIGH,
    )

    assert plan.goal_id == "goal-1"
    assert plan.name == "Rodent Removal Plan"


def test_empty_tasks():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
    )

    assert plan.tasks == []


def test_add_tasks():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Inspect",
                description="Inspect property.",
            ),
            Task(
                name="Seal Entry",
                description="Seal entry points.",
            ),
        ],
    )

    assert len(plan.tasks) == 2


def test_empty_constraints():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
    )

    assert plan.constraints == []


def test_constraints():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
        constraints=[
            Constraint(
                name="Safety",
                description="Use PPE.",
            )
        ],
    )

    assert len(plan.constraints) == 1


def test_plan_serialization():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
    )

    dumped = plan.model_dump()

    assert dumped["goal_id"] == "goal-1"


def test_plan_copy():

    plan = Plan(
        goal_id="goal-1",
        name="Plan",
        description="Description",
        priority=GoalPriority.HIGH,
    )

    copied = plan.model_copy()

    assert copied == plan

def test_plan_defaults_are_independent():

    plan1 = Plan(
        goal_id="1",
        name="Plan A",
        description="A",
        priority=GoalPriority.HIGH,
    )

    plan2 = Plan(
        goal_id="2",
        name="Plan B",
        description="B",
        priority=GoalPriority.HIGH,
    )

    plan1.tasks.append(
        Task(
            name="Inspect",
            description="Inspect.",
        
        )
    )

    assert plan2.tasks == []