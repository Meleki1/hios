import pytest

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.execution.models.action import Action
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.assistant.response.assistant_action_response_builder import AssistantActionResponseBuilder
from hios.capabilities.execution.models.action import Action, ActionType
from hios.capabilities.execution.default import DefaultExecutor
from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.planning.default_planner import DefaultPlanner

def test_create_execution(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    assert execution.decision == decision

def test_default_status(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    assert execution.status == ExecutionStatus.PENDING

def test_default_actions(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    assert execution.actions == []

def test_add_actions(
    decision,
):

    execution = Execution(
        decision=decision,
        actions=[
            Action(
                name="Inspect",
                description="Inspect property.",
            ),
            Action(
                name="Seal",
                description="Seal entry.",
            ),
        ],
    )

    assert len(execution.actions) == 2

def test_execution_serialization(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    dumped = execution.model_dump()

    assert dumped["status"] == ExecutionStatus.PENDING

def test_execution_copy(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    copied = execution.model_copy()

    assert copied == execution

def test_execution_equality(
    decision,
):

    execution = Execution(
        decision=decision,
    )

    copied = execution.model_copy()

    assert copied == execution

def test_default_actions_are_independent(
    decision,
):

    execution1 = Execution(
        decision=decision,
    )

    execution2 = Execution(
        decision=decision,
    )

    execution1.actions.append(
        Action(
            name="Inspect",
            description="Inspect property.",
        )
    )

    assert execution2.actions == []

def test_visual_evidence_flows_to_image_request_response():

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

    plan = plans[0]

    decision = Decision(
        plan=plan,
        rationale="Visual evidence is required.",
        score=1.0,
    )

    execution = Execution(
        decision=decision,
    )

    executed = DefaultExecutor().execute(
        execution,
    )

    assert executed.actions
    assert (
        executed.actions[0].action_type
        == ActionType.IMAGE_REQUEST
    )

    response = AssistantActionResponseBuilder().build(
        actions=executed.actions,
        conversation_id="conversation-1",
    )

    assert response is not None
    assert response.capability == "image_diagnosis"
    assert response.metadata["requires_user_input"] is True
    assert "photo" in response.message.lower()

def test_gather_more_information_is_user_input():
    executor = DefaultExecutor()

    assert (
        executor._get_action_type(
            "Gather more information",
        )
        == ActionType.USER_INPUT
    )

def test_request_image_evidence_is_image_request():
    executor = DefaultExecutor()

    assert (
        executor._get_action_type(
            "Request Image Evidence",
        )
        == ActionType.IMAGE_REQUEST
    )