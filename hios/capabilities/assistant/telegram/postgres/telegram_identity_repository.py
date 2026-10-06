from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.assistant.telegram.models import (
    TelegramIdentity,
)
from hios.capabilities.assistant.telegram.telegram_identity_repository import (
    TelegramIdentityRepository,
)
from hios.capabilities.assistant.telegram.postgres.models.telegram_identity import (
    TelegramIdentityRecord,
)


class PostgresTelegramIdentityRepository(
    TelegramIdentityRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_by_telegram_user_id(
        self,
        telegram_user_id: str,
    ) -> TelegramIdentity | None:

        stmt = select(TelegramIdentityRecord).where(
            TelegramIdentityRecord.telegram_user_id
            == telegram_user_id,
        )

        result = await self._session.execute(stmt)

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return self._to_domain(record)

    async def save(
        self,
        identity: TelegramIdentity,
    ) -> TelegramIdentity:

        now = datetime.now(timezone.utc)

        record = TelegramIdentityRecord(
            telegram_user_id=identity.telegram_user_id,
            subject_id=identity.subject_id,
            home_id=identity.home_id,
            created_at=now,
            updated_at=now,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    @staticmethod
    def _to_domain(
        record: TelegramIdentityRecord,
    ) -> TelegramIdentity:

        return TelegramIdentity(
            telegram_user_id=record.telegram_user_id,
            subject_id=record.subject_id,
            home_id=record.home_id,
        )
