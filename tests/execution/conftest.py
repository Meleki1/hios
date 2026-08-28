import pytest

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.models.task import Task

@pytest.fixture
def plan():
    return Plan(
        goal_id="goal-1",
        name="Rodent Removal Plan",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )


@pytest.fixture
def decision(plan):
    return Decision(
        plan=plan,
        rationale="Highest priority.",
        score=1.0,
    )


@pytest.fixture
def execution(decision):
    return Execution(
        decision=decision,
    )

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