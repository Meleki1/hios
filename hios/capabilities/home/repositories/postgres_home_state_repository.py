from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.home.models.home_state import (
    HomeState,
)

from hios.capabilities.home.repositories.home_state_repository import (
    HomeStateRepository,
)

from hios.capabilities.home.persistence.models.home_state_record import (
    HomeStateRecord,
)


class PostgresHomeStateRepository(
    HomeStateRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        state: HomeState,
    ) -> HomeState:

        record = HomeStateRecord(
            id=state.id,
            home_id=state.home_id,
            status=state.status,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeState | None:

        stmt = (
            select(HomeStateRecord)
            .where(
                HomeStateRecord.home_id
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
        record: HomeStateRecord,
    ) -> HomeState:

        return HomeState(
            id=record.id,
            home_id=record.home_id,
            status=record.status,
        )