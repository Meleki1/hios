from abc import ABC, abstractmethod

from hios.capabilities.assistant.models.interaction_routing import (
    InteractionRoutingRequest,
    InteractionRoutingResult,
)


class InteractionRouter(ABC):

    @abstractmethod
    async def route(
        self,
        request: InteractionRoutingRequest,
    ) -> InteractionRoutingResult:
        raise NotImplementedError