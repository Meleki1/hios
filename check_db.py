import asyncio

from sqlalchemy import text
from hios.db.session import engine


async def main():
    async with engine.connect() as connection:
        result = await connection.execute(
            text(
                "SELECT current_database(), "
                "current_user, version()"
            )
        )

        print(result.one())

    await engine.dispose()


asyncio.run(main())