import pytest

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
async def test_timeline_service_records_entry():

    repository = FakeTimelineRepository()

    service = TimelineService(
        repository=repository,
    )

    entry = TimelineEntry(
        subject_id="household-1",
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    result = await service.record(entry)

    assert result is entry

    assert repository.entries == [
        entry
    ]


@pytest.mark.asyncio
async def test_timeline_service_gets_subject_timeline():

    repository = FakeTimelineRepository()

    service = TimelineService(
        repository=repository,
    )

    first = TimelineEntry(
        subject_id="household-1",
        event_type="risk",
        event_name="risk_assessed",
        state="high",
        description="Risk assessed",
    )

    second = TimelineEntry(
        subject_id="household-1",
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
    )

    other = TimelineEntry(
        subject_id="household-2",
        event_type="risk",
        event_name="risk_assessed",
        state="low",
        description="Risk assessed",
    )

    await service.record(first)
    await service.record(second)
    await service.record(other)

    results = await service.get_by_subject(
        "household-1",
    )

    assert results == [
        first,
        second,
    ]