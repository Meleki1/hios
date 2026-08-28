from abc import ABC, abstractmethod

from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)


class TimelineRepository(ABC):

    @abstractmethod
    async def save(
        self,
        entry: TimelineEntry,
    ) -> TimelineEntry:
        raise NotImplementedError

    @abstractmethod
    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[TimelineEntry]:
        raise NotImplementedError