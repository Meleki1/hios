import pytest
from hios.capabilities.execution.default import DefaultExecutor
from hios.capabilities.execution.executor import Executor
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus
from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.models.task import Task
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.execution.models.action import (
    Action,
    ActionType,
)

@pytest.fixture
def executor():

    return DefaultExecutor()

def test_returns_execution(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    assert result == execution

def test_preserves_decision(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    assert result.decision == execution.decision

def test_generates_actions(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    assert len(result.actions) == len(
        execution.decision.plan.tasks
    )

def test_action_names_match_tasks(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    for action, task in zip(
        result.actions,
        execution.decision.plan.tasks,
    ):

        assert action.name == task.name

def test_action_descriptions_match_tasks(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    for action, task in zip(
        result.actions,
        execution.decision.plan.tasks,
    ):

        assert action.description == task.description

def test_actions_are_pending(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    assert all(
        action.status == ExecutionStatus.PENDING
        for action in result.actions
    )

def test_execution_status_remains_pending(
    executor,
    execution,
):

    result = executor.execute(
        execution,
    )

    assert (
        result.status
        == ExecutionStatus.PENDING
    )

def test_empty_tasks(
    executor,
    decision,
):

    execution = Execution(
        decision=decision,
    )

    result = executor.execute(
        execution,
    )

    assert result.actions == []

def test_generates_image_evidence_action(
    executor,
):
    plan = Plan(
        goal_id="goal-visual-1",
        name="Gather Visual Evidence",
        description="Gather visual evidence.",
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Request Image Evidence",
                description=(
                    "Request an image of the affected "
                    "area to gather visual evidence."
                ),
                required=True,
            ),
        ],
    )

    decision = Decision(
        
        plan=plan,
        rationale="Highest priority plan.",
        score=0.95,
    )
    

    execution = Execution(
        decision=decision,
    )

    result = executor.execute(execution)

    assert len(result.actions) == 1

    action = result.actions[0]

    assert action.name == "Request Image Evidence"
    assert "image" in action.description.lower()
    assert action.status == ExecutionStatus.PENDING

@pytest.fixture
def image_plan():
    return Plan(
        goal_id="goal-visual-1",
        name="Gather Visual Evidence",
        description="Gather visual evidence.",
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Request Image Evidence",
                description=(
                    "Request an image of the affected area "
                    "to gather visual evidence."
                ),
                required=True,
            ),
        ],
    )

@pytest.fixture
def image_decision(image_plan):
    return Decision(
        plan=image_plan,
        rationale="Visual evidence is required.",
        score=1.0,
    )

@pytest.fixture
def image_execution(image_decision):
    return Execution(
        decision=image_decision,
    )

def test_image_evidence_task_creates_image_request_action(
    executor,
    image_execution,
):
    result = executor.execute(image_execution)

    assert len(result.actions) == 1

    action = result.actions[0]

    assert action.name == "Request Image Evidence"
    assert action.action_type == ActionType.IMAGE_REQUEST

@pytest.fixture
def inspection_plan():
    return Plan(
        goal_id="goal-1",
        name="Inspection Plan",
        description="Inspect the property.",
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Inspect property",
                description="Inspect the affected property.",
            ),
        ],
    )


@pytest.fixture
def inspection_decision(inspection_plan):
    return Decision(
        plan=inspection_plan,
        rationale="Inspection is required.",
        score=1.0,
    )

@pytest.fixture
def inspection_execution(inspection_decision):
    return Execution(
        decision=inspection_decision,
    )

def test_normal_task_creates_system_operation_action(
    executor,
    inspection_execution,
):
    result = executor.execute(inspection_execution)

    assert len(result.actions) == 1

    action = result.actions[0]

    assert action.name == "Inspect property"
    assert action.action_type == ActionType.SYSTEM_OPERATION