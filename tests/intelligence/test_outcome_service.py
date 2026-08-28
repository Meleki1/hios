import pytest

from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)
from hios.capabilities.intelligence.outcome.outcome_service import (
    OutcomeService,
)
from hios.capabilities.intelligence.outcome.outcome_repository import (
    OutcomeRepository,
)
from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)

from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)

from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)

from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)

from hios.core.events.event_publisher import (
    EventPublisher,
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


class FakeSubscriber:

    def __init__(self):
        self.events = []

    async def listen(
        self,
        event: BaseEvent,
    ):
        self.events.append(event)

class FakeOutcomeRepository(
    OutcomeRepository,
):

    def __init__(self):
        self.saved = None
        self.outcomes = []

    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:

        self.saved = outcome
        self.outcomes.append(outcome)

        return outcome

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:

        for outcome in self.outcomes:
            if outcome.prediction_id == prediction_id:
                return outcome

        return None


@pytest.mark.asyncio
async def test_outcome_service_records_outcome():

    repository = FakeOutcomeRepository()

    service = OutcomeService(
        repository=repository,
    )

    outcome = Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    result = await service.record(
        outcome,
    )

    assert result is outcome
    assert repository.saved is outcome


@pytest.mark.asyncio
async def test_outcome_service_gets_outcome_by_prediction():

    repository = FakeOutcomeRepository()

    service = OutcomeService(
        repository=repository,
    )

    outcome = Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    await service.record(outcome)

    result = await service.get_by_prediction(
        "prediction-1",
    )

    assert result is outcome



@pytest.mark.asyncio
async def test_outcome_service_publishes_outcome_recorded_event():

    repository = FakeOutcomeRepository()
    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    service = OutcomeService(
        repository=repository,
        event_publisher=publisher,
    )

    outcome = Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    result = await service.record(
        outcome,
    )

    assert len(subscriber.events) == 1

    event = subscriber.events[0]

    assert event.event_type == "outcome"
    assert event.event_name == "outcome_recorded"
    assert event.state == "observed"
    assert event.subject_id == result.subject_id
    assert event.resource_id == result.id
    assert event.resource_type == "outcome"

@pytest.mark.asyncio
async def test_outcome_service_records_outcome_in_timeline():

    outcome_repository = FakeOutcomeRepository()
    timeline_repository = FakeTimelineRepository()

    publisher = EventPublisher()

    timeline_service = TimelineService(
        repository=timeline_repository,
    )

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    publisher.subscribe(
        timeline_listener,
    )

    outcome_service = OutcomeService(
        repository=outcome_repository,
        event_publisher=publisher,
    )

    outcome = Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    result = await outcome_service.record(
        outcome,
    )

    assert result is outcome

    assert len(
        timeline_repository.entries
    ) == 1

    entry = (
        timeline_repository.entries[0]
    )

    assert entry.subject_id == (
        outcome.subject_id
    )

    assert entry.event_type == "outcome"

    assert entry.event_name == (
        "outcome_recorded"
    )

    assert entry.state == "observed"

    assert entry.resource_id == (
        outcome.id
    )

    assert entry.resource_type == "outcome"