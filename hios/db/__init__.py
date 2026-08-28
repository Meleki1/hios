from hios.db.base import Base
from .session import SessionLocal, engine


async def initialize_database():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )


__all__ = [
    "Base",
    "SessionLocal",
    "engine",
]