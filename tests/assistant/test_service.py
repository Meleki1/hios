import pytest

from hios.capabilities.assistant.models.assistant_request import (
    HomeAssistantRequest,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.assistant.service import (
    AssistantService,
)

class FakeEventPublisher:

    def __init__(self):
        self.events = []

    async def publish(self, event):
        self.events.append(event)

class FakeGraph:

    async def ainvoke(
        self,
        state,
    ):

        self.state = state

        return {
            "response": HomeAssistantResponse(
                message="Response from HIA.",
                conversation_id=state.get(
                    "conversation_id",
                ),
                capability="pest_control",
                metadata={},
            )
        }


@pytest.mark.asyncio
async def test_assistant_service_executes_graph():

    graph = FakeGraph()

    service = AssistantService(
        graph=graph,
    )

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        conversation_id="conversation-123",
        message=(
            "I found droppings in my kitchen."
        ),
    )

    response = await service.execute(
        request,
    )

    assert isinstance(
        response,
        HomeAssistantResponse,
    )

    assert response.message == (
        "Response from HIA."
    )

    assert response.conversation_id == (
        "conversation-123"
    )

    assert response.capability == (
        "pest_control"
    )

    assert graph.state["subject_id"] == (
        "subject-123"
    )

    assert graph.state["home_id"] == (
        "home-123"
    )

    assert graph.state["message"] == (
        "I found droppings in my kitchen."
    )

@pytest.mark.asyncio
async def test_assistant_service_executes_graph():

    graph = FakeGraph()
    publisher = FakeEventPublisher()

    service = AssistantService(
        graph=graph,
        event_publisher=publisher,
    )

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        conversation_id="conversation-123",
        message=(
            "I found droppings in my kitchen."
        ),
    )

    response = await service.execute(
        request,
    )

    assert isinstance(
        response,
        HomeAssistantResponse,
    )

    assert response.message == (
        "Response from HIA."
    )

    assert len(publisher.events) == 1

    event = publisher.events[0]

    assert event.event_type == (
        "conversation"
    )

    assert event.event_name == (
        "message_received"
    )

    assert event.state == (
        "observed"
    )

    assert event.subject_id == (
        "subject-123"
    )

    assert event.resource_id == (
        "conversation-123"
    )

    assert event.resource_type == (
        "conversation"
    )

    assert event.description == (
        "I found droppings in my kitchen."
    )