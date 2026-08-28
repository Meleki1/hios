import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from hios.core.config import get_settings


async def main():
    engine = create_async_engine(
        get_settings().database_url,
    )

    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename
                """
            )
        )

        tables = result.fetchall()

        print("TABLES:")
        for row in tables:
            print(f"- {row[0]}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())