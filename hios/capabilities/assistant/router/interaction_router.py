from abc import ABC, abstractmethod

from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)


class InteractionRouter(ABC):

    @abstractmethod
    def route(
        self,
        message: str,
    ) -> AssistantDomain:

        raise NotImplementedError