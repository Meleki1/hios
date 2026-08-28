from dataclasses import dataclass

from hios.capabilities.assistant.graph.state import (
    HomeAssistantState,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)


@dataclass
class ChatRequest:
    subject_id: str
    home_id: str
    message: str
    conversation_id: str | None = None
    image: bytes | None = None


class HomeAssistantChat:

    def __init__(
        self,
        graph,
    ):
        self._graph = graph

    async def send(
        self,
        request: ChatRequest,
    ) -> HomeAssistantResponse:

        state: HomeAssistantState = {
            "subject_id": request.subject_id,
            "home_id": request.home_id,
            "conversation_id": request.conversation_id,
            "message": request.message,
            "image": request.image,
        }

        result = await self._graph.ainvoke(
            state,
        )

        response = result.get("response")

        if response is None:
            raise RuntimeError(
                "Home Assistant graph returned no response"
            )

        return response