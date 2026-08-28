from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.home.models.home import Home
from hios.capabilities.home.repositories.home_repository import (
    HomeRepository,
)
from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)


class PostgresHomeRepository(HomeRepository):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        home: Home,
    ) -> Home:

        record = HomeRecord(
            id=home.id,
            name=home.name,
            home_type=home.home_type,
            description=home.description,
            status=home.status,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get(
        self,
        home_id: str,
    ) -> Home | None:

        stmt = (
            select(HomeRecord)
            .where(
                HomeRecord.id == home_id,
            )
        )

        result = await self._session.execute(
            stmt,
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return self._to_domain(record)

    @staticmethod
    def _to_domain(
        record: HomeRecord,
    ) -> Home:

        return Home(
            id=record.id,
            name=record.name,
            home_type=record.home_type,
            description=record.description,
            status=record.status,
        )