import pytest

from hios.capabilities.memory.embedding.embedder import Embedder


class FakeEmbedder(Embedder):

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        return [
            0.1,
            0.2,
            0.3,
        ]


@pytest.mark.asyncio
async def test_embed_returns_list():

    embedder = FakeEmbedder()

    embedding = await embedder.embed(
        "Inspect kitchens first.",
    )

    assert isinstance(
        embedding,
        list,
    )

@pytest.mark.asyncio
async def test_embedding_is_not_empty():

    embedder = FakeEmbedder()

    embedding = await embedder.embed(
        "Inspect kitchens first.",
    )

    assert len(embedding) > 0

@pytest.mark.asyncio
async def test_embedding_contains_floats():

    embedder = FakeEmbedder()

    embedding = await embedder.embed(
        "Inspect kitchens first.",
    )

    assert all(
        isinstance(
            value,
            float,
        )
        for value in embedding
    )