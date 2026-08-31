from hios.capabilities.assistant.response.assistant_action_response_builder import (
    AssistantActionResponseBuilder,
)
from hios.capabilities.execution.models.action import Action, ActionType
from hios.capabilities.safety.contract.result import (
    SafetyGuidanceResult,
)


def test_image_request_creates_assistant_response():

    action = Action(
        action_type=ActionType.IMAGE_REQUEST,
        name="Request Image Evidence",
        description=(
            "Request an image of the affected area "
            "to gather visual evidence."
        ),
    )

    response = AssistantActionResponseBuilder().build(
        actions=[action],
        conversation_id="conversation-1",
    )

    assert response is not None
    assert "photo" in response.message.lower()
    assert response.capability == "image_diagnosis"

def test_image_request_response_contains_action_metadata():

    action = Action(
        action_type=ActionType.IMAGE_REQUEST,
        name="Request Image Evidence",
        description="Request an image.",
    )

    response = AssistantActionResponseBuilder().build(
        actions=[action],
        conversation_id="conversation-1",
    )

    assert response.metadata["action_type"] == (
        ActionType.IMAGE_REQUEST.value
    )
    assert response.metadata["requires_user_input"] is True

def test_normal_action_returns_no_special_response():

    action = Action(
        action_type=ActionType.SYSTEM_OPERATION,
        name="Inspect property",
        description="Inspect the affected property.",
    )

    response = AssistantActionResponseBuilder().build(
        actions=[action],
        conversation_id="conversation-1",
    )

    assert response is None

def test_empty_actions_returns_no_response():

    response = AssistantActionResponseBuilder().build(
        actions=[],
        conversation_id="conversation-1",
    )

    assert response is None

def test_image_request_response_includes_safety_guidance():
    builder = AssistantActionResponseBuilder()

    action = Action(
        action_type=ActionType.IMAGE_REQUEST,
        name="Request Image Evidence",
        description="Request an image.",
    )

    safety_guidance = SafetyGuidanceResult(
        guidance=[
            "Avoid touching the droppings directly.",
            "Keep children and pets away from the area.",
        ],
    )

    response = builder.build(
        actions=[action],
        safety_guidance=safety_guidance,
        conversation_id="conversation-1",
    )

    assert response is not None
    assert "Avoid touching the droppings directly." in response.message
    assert "Keep children and pets away from the area." in response.message
    assert "photo" in response.message.lower()