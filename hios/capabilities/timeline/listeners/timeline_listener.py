from hios.core.events.base_event import BaseEvent
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)


class TimelineListener:

    def __init__(
        self,
        service: TimelineService,
    ):
        self._service = service

    async def listen(
        self,
        event: BaseEvent,
    ) -> None:

        entry = TimelineEntry(
            subject_id=event.subject_id,
            event_type=event.event_type,
            event_name=event.event_name,
            state=event.state,
            description=event.description,
            resource_id=event.resource_id,
            resource_type=event.resource_type,
            created_at=event.created_at,
        )

        await self._service.record(
            entry,
        )