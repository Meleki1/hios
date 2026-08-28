from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)
from hios.db.models.timeline_entry import (
    TimelineEntryRecord,
)


class PostgresTimelineRepository(
    TimelineRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        entry: TimelineEntry,
    ) -> TimelineEntry:

        record = TimelineEntryRecord(
            id=entry.id,
            subject_id=entry.subject_id,
            event_type=entry.event_type,
            event_name=entry.event_name,
            state=entry.state,
            description=entry.description,
            resource_id=entry.resource_id,
            resource_type=entry.resource_type,
            created_at=entry.created_at,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[TimelineEntry]:

        stmt = (
            select(TimelineEntryRecord)
            .where(
                TimelineEntryRecord.subject_id == subject_id,
            )
            .order_by(
                TimelineEntryRecord.created_at.asc(),
            )
        )

        result = await self._session.execute(stmt)

        records = result.scalars().all()

        return [
            self._to_domain(record)
            for record in records
        ]

    @staticmethod
    def _to_domain(
        record: TimelineEntryRecord,
    ) -> TimelineEntry:

        return TimelineEntry(
            id=record.id,
            subject_id=record.subject_id,
            event_type=record.event_type,
            event_name=record.event_name,
            state=record.state,
            description=record.description,
            resource_id=record.resource_id,
            resource_type=record.resource_type,
            created_at=record.created_at,
        )