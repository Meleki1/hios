from pydantic import Field

from hios.shared.base import HIOSModel


class HomeAssistantResponse(HIOSModel):

    message: str

    conversation_id: str | None = None

    capability: str | None = None

    metadata: dict = Field(
        default_factory=dict,
    )