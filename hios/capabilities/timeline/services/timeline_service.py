from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)


class TimelineService:

    def __init__(
        self,
        repository: TimelineRepository,
    ):
        self._repository = repository

    async def record(
        self,
        entry: TimelineEntry,
    ) -> TimelineEntry:

        return await self._repository.save(
            entry,
        )

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[TimelineEntry]:

        return await self._repository.get_by_subject(
            subject_id,
        )