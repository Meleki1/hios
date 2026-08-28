from openai import AsyncOpenAI

from hios.capabilities.assistant.llm.contract import (
    AssistantLLM,
)


class OpenAIAssistantLLM(AssistantLLM):

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
    ) -> None:
        self._client = AsyncOpenAI(
            api_key=api_key,
        )
        self._model = model

    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = await self._client.responses.create(
            model=self._model,
            instructions=system_prompt,
            input=user_prompt,
        )

        return response.output_text