import pytest

from hios.core.events.base_event import BaseEvent
from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)


class FakeTimelineRepository(
    TimelineRepository,
):

    def __init__(self):
        self.entries = []

    async def save(
        self,
        entry: TimelineEntry,
    ) -> TimelineEntry:

        self.entries.append(entry)

        return entry

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[TimelineEntry]:

        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]


@pytest.mark.asyncio
async def test_timeline_listener_converts_event_to_timeline_entry():

    repository = FakeTimelineRepository()

    service = TimelineService(
        repository=repository,
    )

    listener = TimelineListener(
        service=service,
    )

    event = BaseEvent(
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        subject_id="household-1",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    await listener.listen(event)

    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == "household-1"
    assert entry.event_type == "prediction"
    assert entry.event_name == "prediction_created"
    assert entry.state == "created"
    assert entry.description == "Prediction created"
    assert entry.resource_id == "prediction-1"
    assert entry.resource_type == "prediction"

    assert entry.created_at == event.created_at


@pytest.mark.asyncio
async def test_timeline_listener_preserves_event_identity():

    repository = FakeTimelineRepository()

    service = TimelineService(
        repository=repository,
    )

    listener = TimelineListener(
        service=service,
    )

    event = BaseEvent(
        event_type="outcome",
        event_name="outcome_recorded",
        state="observed",
        description="Pest control need occurred",
        subject_id="household-2",
        resource_id="outcome-1",
        resource_type="outcome",
    )

    await listener.listen(event)

    entry = repository.entries[0]

    assert entry.event_type == "outcome"
    assert entry.event_name == "outcome_recorded"
    assert entry.state == "observed"
    assert entry.subject_id == "household-2"
    assert entry.resource_id == "outcome-1"
    assert entry.resource_type == "outcome"


