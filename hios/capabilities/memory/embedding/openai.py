from __future__ import annotations

from openai import AsyncOpenAI

from hios.capabilities.memory.embedding.embedder import (
    Embedder,
)


class OpenAIEmbedder(Embedder):

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ):
        self._client = AsyncOpenAI(
            api_key=api_key,
        )

        self._model = model

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        response = await self._client.embeddings.create(
            model=self._model,
            input=text,
        )

        return response.data[0].embedding