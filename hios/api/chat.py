from fastapi import APIRouter, Depends
from pydantic import BaseModel

from hios.capabilities.assistant.chat import (
    ChatRequest,
    HomeAssistantChat,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.api.dependencies import (
    get_home_assistant_chat,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


class ChatMessageRequest(BaseModel):
    subject_id: str
    home_id: str
    message: str
    conversation_id: str | None = None



@router.post(
    "",
    response_model=HomeAssistantResponse,
)
async def chat(
    request: ChatMessageRequest,
    assistant: HomeAssistantChat = Depends(
        get_home_assistant_chat,
    ),
) -> HomeAssistantResponse:

    result = await assistant.send(
        ChatRequest(
            subject_id=request.subject_id,
            home_id=request.home_id,
            message=request.message,
            conversation_id=request.conversation_id,
        )
    )

    return result