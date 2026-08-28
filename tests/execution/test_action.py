import pytest

from hios.capabilities.execution.models.action import Action, ActionType
from hios.capabilities.execution.models.status import ExecutionStatus


def test_create_action():

    action = Action(
        name="Navigate",
        description="Open the target website.",
    )

    assert action.name == "Navigate"
    assert action.description == "Open the target website."


def test_action_generates_unique_id():

    action1 = Action(
        name="A",
        description="Action A",
    )

    action2 = Action(
        name="B",
        description="Action B",
    )

    assert action1.id != action2.id


def test_default_status():

    action = Action(
        name="Navigate",
        description="Open website.",
    )

    assert action.status == ExecutionStatus.PENDING


def test_parameters_default_empty():

    action = Action(
        name="Navigate",
        description="Open website.",
    )

    assert action.parameters == {}


def test_parameters_can_be_supplied():

    action = Action(
        name="Navigate",
        description="Open website.",
        parameters={
            "url": "https://example.com",
        },
    )

    assert action.parameters["url"] == "https://example.com"


def test_action_serialization():

    action = Action(
        name="Navigate",
        description="Open website.",
    )

    dumped = action.model_dump()

    assert dumped["name"] == "Navigate"
    assert dumped["status"] == ExecutionStatus.PENDING


def test_action_copy():

    action = Action(
        name="Navigate",
        description="Open website.",
    )

    copied = action.model_copy()

    assert copied == action


def test_action_equality():

    action = Action(
        name="Navigate",
        description="Open website.",
    )

    copied = action.model_copy()

    assert copied == action


def test_default_parameters_are_independent():

    action1 = Action(
        name="A",
        description="Action A",
    )

    action2 = Action(
        name="B",
        description="Action B",
    )

    action1.parameters["url"] = "https://example.com"

    assert action2.parameters == {}

def test_action_defaults_to_system_operation():

    action = Action(
        id="action-1",
        name="Inspect property",
        description="Inspect the property.",
    )

    assert action.action_type == ActionType.SYSTEM_OPERATION

def test_action_supports_image_request():

    action = Action(
        id="action-1",
        name="Request affected-area image",
        description="Ask the user to provide an image.",
        action_type=ActionType.IMAGE_REQUEST,
    )

    assert action.action_type == ActionType.IMAGE_REQUEST

def test_image_request_preserves_parameters():

    action = Action(
        id="action-1",
        name="Request affected-area image",
        description="Ask the user to provide an image.",
        action_type=ActionType.IMAGE_REQUEST,
        parameters={
            "purpose": "identify suspected pest evidence",
            "location": "kitchen",
        },
    )

    assert action.parameters == {
        "purpose": "identify suspected pest evidence",
        "location": "kitchen",
    }

def test_action_type_serializes_to_string():

    action = Action(
        id="action-1",
        name="Request image",
        description="Request an image from the user.",
        action_type=ActionType.IMAGE_REQUEST,
    )

    data = action.model_dump()

    assert data["action_type"] == "image_request"

def test_action_types():

    assert ActionType.SYSTEM_OPERATION.value == "system_operation"
    assert ActionType.USER_INPUT.value == "user_input"
    assert ActionType.IMAGE_REQUEST.value == "image_request"