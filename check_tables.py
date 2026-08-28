import asyncio

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from hios.core.config import get_settings


async def main():
    settings = get_settings()

    engine = create_async_engine(
        settings.database_url,
    )

    async with engine.connect() as connection:
        tables = await connection.run_sync(
            lambda conn: inspect(conn).get_table_names()
        )

        print(tables)

    await engine.dispose()


asyncio.run(main())