from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.repositories.home_information_repository import (
    HomeInformationRepository,
)
from hios.capabilities.home.persistence.models.home_information_record import (
    HomeInformationRecord,
)


class PostgresHomeInformationRepository(
    HomeInformationRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        information: HomeInformation,
    ) -> HomeInformation:

        record = HomeInformationRecord(
            id=information.id,
            home_id=information.home_id,
            country=information.country,
            city=information.city,
            address=information.address,
            postcode=information.postcode,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeInformation | None:

        stmt = (
            select(HomeInformationRecord)
            .where(
                HomeInformationRecord.home_id
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
        record: HomeInformationRecord,
    ) -> HomeInformation:

        return HomeInformation(
            id=record.id,
            home_id=record.home_id,
            country=record.country,
            city=record.city,
            address=record.address,
            postcode=record.postcode,
        )