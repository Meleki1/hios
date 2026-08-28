import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy import delete
from hios.db.models.memory_entry import MemoryRecord

from hios.db.base import Base
from sqlalchemy.pool import NullPool


from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)

from hios.capabilities.home.persistence.models.home_information_record import (
    HomeInformationRecord,
)

from hios.capabilities.home.persistence.models.home_state_record import (
    HomeStateRecord,
)
from hios.db.models.home_property_reference import (
    HomePropertyReferenceRecord,
)
from hios.capabilities.learning.postgres.models.learning_record import (
    LearningRecordModel,
)
from hios.capabilities.learning.postgres.models.learning_insight_record import (
    LearningInsightModel,
)
from hios.core.audit.postgres.models.audit_record import AuditRecord as AuditRecordModel
from hios.capabilities.maintenance.postgres.models.maintenance_record import (
    MaintenanceRecord,
)



TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:2511@127.0.0.1:5433/hios_test"
)




engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)




@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True,
)
async def setup_database():

    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all,
        )

    yield



@pytest_asyncio.fixture
async def session():

    async with SessionLocal() as session:
        yield session

        await session.rollback()

        await session.execute(
            delete(MaintenanceRecord)
        )

        await session.execute(
            delete(LearningInsightModel)
        )

        await session.commit()