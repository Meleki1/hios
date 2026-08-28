import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine(
    "postgresql+asyncpg://postgres:2511@localhost:5432/hios_test"
)


async def main():

    async with engine.connect() as conn:

        result = await conn.execute(
            text("SELECT version()")
        )

        print(result.scalar())


asyncio.run(main())