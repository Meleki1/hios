from pydantic import Field

from hios.shared.base import HIOSModel


class HomeAssistantRequest(HIOSModel):

    subject_id: str

    home_id: str

    message: str

    conversation_id: str | None = None

    metadata: dict = Field(
        default_factory=dict,
    )