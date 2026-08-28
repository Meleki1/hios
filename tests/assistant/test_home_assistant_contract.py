from hios.capabilities.assistant.models.assistant_request import (
    HomeAssistantRequest,
)

from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)

from hios.capabilities.assistant.models.assistant_domain import AssistantDomain


def test_home_assistant_request_requires_home_and_subject():

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="Hello",
    )

    assert request.subject_id == "subject-123"
    assert request.home_id == "home-123"
    assert request.message == "Hello"

def test_home_assistant_response_contains_message():

    response = HomeAssistantResponse(
        message=(
            "Hello! I'm HIOS, your Home Intelligence "
            "Operating System."
        ),
        capability="conversation",
    )

    assert response.message.startswith(
        "Hello!"
    )

    assert response.capability == "conversation"

def test_assistant_domain_supports_current_pest_control_scope():

    assert (
        AssistantDomain.PEST_CONTROL.value
        == "pest_control"
    )

    assert (
        AssistantDomain.UNSUPPORTED.value
        == "unsupported"
    )