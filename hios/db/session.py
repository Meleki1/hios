from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from hios.core.config import get_settings


settings = get_settings()


engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)