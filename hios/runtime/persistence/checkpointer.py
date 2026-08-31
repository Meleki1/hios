from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from hios.core.config import get_settings


@asynccontextmanager
async def create_checkpointer() -> AsyncIterator[
    AsyncPostgresSaver
]:
    settings = get_settings()

    database_url = settings.database_url

    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace(
            "postgresql+asyncpg://",
            "postgresql://",
            1,
        )
        
    elif database_url.startswith("postgres+asyncpg://"):
        database_url = database_url.replace(
            "postgres+asyncpg://",
            "postgresql://",
            1,
        )

    async with AsyncPostgresSaver.from_conn_string(
        database_url,
    ) as checkpointer:
        yield checkpointer