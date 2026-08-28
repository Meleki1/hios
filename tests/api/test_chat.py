from fastapi import FastAPI
from fastapi.testclient import TestClient

from hios.api.chat import router
from hios.api.dependencies import get_home_assistant_chat
from hios.capabilities.assistant.chat import (
    HomeAssistantChat,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)


class FakeGraph:

    async def ainvoke(
        self,
        state,
    ):
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


def test_chat_endpoint():

    app = FastAPI()

    app.include_router(router)

    assistant = HomeAssistantChat(
        graph=FakeGraph(),
    )

    app.dependency_overrides[
        get_home_assistant_chat
    ] = lambda: assistant

    client = TestClient(app)

    response = client.post(
        "/chat",
        json={
            "subject_id": "subject-1",
            "home_id": "home-1",
            "conversation_id": "conversation-1",
            "message": "Hello",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Hello from Home Assistant."
    )

    assert data["conversation_id"] == (
        "conversation-1"
    )

    assert data["capability"] == "assistant"