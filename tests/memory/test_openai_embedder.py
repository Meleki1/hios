import pytest

from hios.capabilities.memory.embedding import (
    OpenAIEmbedder,
)

from hios.core.config import get_settings


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openai_embedder():

    settings = get_settings()

    embedder = OpenAIEmbedder(
        api_key=settings.openai_api_key,
    )

    embedding = await embedder.embed(
        "Inspect kitchens first.",
    )

    assert len(embedding) > 100