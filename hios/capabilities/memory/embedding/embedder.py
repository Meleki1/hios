from __future__ import annotations

from abc import ABC, abstractmethod
from openai import AsyncOpenAI


class Embedder(ABC):

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> list[float]:
        raise NotImplementedError




class OpenAIEmbedder:
    def __init__(
        self,
        api_key: str,
    ):
        self._client = AsyncOpenAI(
            api_key=api_key,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:
        response = await self._client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding