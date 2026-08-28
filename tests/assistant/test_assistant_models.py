from hios.capabilities.assistant.models.assistant_request import (
    HomeAssistantRequest,
)


def test_assistant_request_contains_required_context():

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="I noticed scratching in the loft.",
    )

    assert request.subject_id == "subject-123"
    assert request.home_id == "home-123"
    assert request.message == (
        "I noticed scratching in the loft."
    )
    assert request.conversation_id is None

def test_assistant_request_accepts_conversation_id():

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="Tell me more about this.",
        conversation_id="conversation-123",
    )

    assert request.conversation_id == (
        "conversation-123"
    )

from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)


def test_assistant_response_contains_message():

    response = HomeAssistantResponse(
        message="I can help you understand what may be happening.",
    )

    assert response.message == (
        "I can help you understand what may be happening."
    )
