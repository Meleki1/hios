import pytest

from hios.capabilities.assistant.chat import (
    ChatRequest,
    HomeAssistantChat,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)


class FakeAssistantGraph:

    def __init__(self):
        self.received_state = None

    async def ainvoke(
        self,
        state,
    ):
        self.received_state = state

        return {
            "response": HomeAssistantResponse(
                message="Hello from Home Assistant.",
                conversation_id=state.get(
                    "conversation_id",
                ),
                capability="assistant",
                metadata={},
            )
        }


@pytest.mark.asyncio
async def test_chat_invokes_home_assistant_graph():

    graph = FakeAssistantGraph()

    chat = HomeAssistantChat(
        graph=graph,
    )

    request = ChatRequest(
        subject_id="subject-1",
        home_id="home-1",
        conversation_id="conversation-1",
        message="Hello",
    )

    response = await chat.send(request)

    assert response.message == (
        "Hello from Home Assistant."
    )

    assert response.conversation_id == (
        "conversation-1"
    )

    assert graph.received_state is not None

    assert graph.received_state["subject_id"] == (
        "subject-1"
    )

    assert graph.received_state["home_id"] == (
        "home-1"
    )

    assert graph.received_state["conversation_id"] == (
        "conversation-1"
    )

    assert graph.received_state["message"] == "Hello"

@pytest.mark.asyncio
async def test_chat_passes_image_to_home_assistant_graph():

    graph = FakeAssistantGraph()

    chat = HomeAssistantChat(
        graph=graph,
    )

    image = b"fake-image-data"

    request = ChatRequest(
        subject_id="subject-1",
        home_id="home-1",
        conversation_id="conversation-1",
        message="What is wrong here?",
        image=image,
    )

    await chat.send(request)

    assert graph.received_state is not None

    assert graph.received_state["image"] == image