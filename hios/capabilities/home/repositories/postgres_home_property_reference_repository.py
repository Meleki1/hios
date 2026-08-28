from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)
from hios.capabilities.home.repositories.home_property_reference_repository import (
    HomePropertyReferenceRepository,
)
from hios.db.models.home_property_reference import (
    HomePropertyReferenceRecord,
)


class PostgresHomePropertyReferenceRepository(
    HomePropertyReferenceRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        reference: HomePropertyReference,
    ) -> HomePropertyReference:

        record = HomePropertyReferenceRecord(
            id=reference.id,
            home_id=reference.home_id,
            uprn=reference.uprn,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomePropertyReference | None:

        stmt = (
            select(HomePropertyReferenceRecord)
            .where(
                HomePropertyReferenceRecord.home_id
                == home_id,
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
        record: HomePropertyReferenceRecord,
    ) -> HomePropertyReference:

        return HomePropertyReference(
            id=record.id,
            home_id=record.home_id,
            uprn=record.uprn,
        )