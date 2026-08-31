from hios.shared.base import HIOSModel

from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)


class InteractionRoutingRequest(HIOSModel):
    message: str
    has_image: bool = False
    previous_domain: AssistantDomain | None = None


class InteractionRoutingResult(HIOSModel):
    domain: AssistantDomain
    confidence: float
    reason: str