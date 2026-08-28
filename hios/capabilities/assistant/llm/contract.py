from abc import ABC, abstractmethod


class AssistantLLM(ABC):

    @abstractmethod
    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        raise NotImplementedError