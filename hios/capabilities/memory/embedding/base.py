from abc import ABC, abstractmethod


class Embedder(ABC):

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> list[float]:
        """Generate an embedding for text."""
        raise NotImplementedError