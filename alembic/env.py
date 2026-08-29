from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import (
    async_engine_from_config,
)
from sqlalchemy import pool

from hios.core.config import get_settings
from hios.db.base import Base
from hios.db.models.memory_entry import MemoryRecord
from hios.capabilities.intelligence.postgres.models.outcome import (
    OutcomeRecord,
)
from hios.capabilities.intelligence.postgres.models.prediction import (
    PredictionRecord,
)

from hios.capabilities.intelligence.postgres.models.prediction_evaluation import (
    PredictionEvaluationRecord,
)
from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)
from hios.capabilities.home.persistence.models.home_information_record import (
    HomeInformationRecord,
)
from hios.capabilities.home.persistence.models.home_state_record import (
    HomeStateRecord,
)
from hios.capabilities.learning.postgres.models.learning_record import (
    LearningRecordModel,
)
from hios.capabilities.learning.postgres.models.learning_insight_record import (
    LearningInsightModel,
)
from hios.capabilities.consent.postgres.models.consent_record import (
    ConsentRecord,
)
from hios.core.audit.postgres.models.audit_record import AuditRecord
from hios.capabilities.maintenance.postgres.models.maintenance_record import (
    MaintenanceRecord,
)
from hios.db.models.timeline_entry import (
    TimelineEntryRecord,
)



config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Importing the model ensures it is registered with Base.metadata.
target_metadata = Base.metadata


settings = get_settings()


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = settings.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in online mode."""

    configuration = config.get_section(
        config.config_ini_section,
    )

    database_url = settings.database_url

    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
            1,
        )
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+asyncpg://",
            1,
        )

    configuration["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations,
        )

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(
        run_migrations_online(),
    )