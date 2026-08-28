import pytest

from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher

from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.core.audit.audit_listener import AuditListener
from hios.core.audit.audit_service import AuditService
from hios.core.audit.models.audit_record import AuditRecord




class FakeAuditRepository:

    def __init__(self):
        self.records: list[AuditRecord] = []

    async def save(
        self,
        audit_record: AuditRecord,
    ) -> AuditRecord:
        self.records.append(audit_record)
        return audit_record

    async def get_by_id(
        self,
        audit_id: str,
    ) -> AuditRecord | None:

        for record in self.records:
            if record.id == audit_id:
                return record

        return None

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[AuditRecord]:

        return [
            record
            for record in self.records
            if record.subject_id == subject_id
        ]

    async def get_by_resource(
        self,
        resource_id: str,
    ) -> list[AuditRecord]:

        return [
            record
            for record in self.records
            if record.resource_id == resource_id
        ]

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
async def test_event_publisher_records_event_in_timeline():

    # --------------------------------------------------
    # Infrastructure
    # --------------------------------------------------

    publisher = EventPublisher()

    repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=repository,
    )

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    publisher.subscribe(
        timeline_listener,
    )

    # --------------------------------------------------
    # Event
    # --------------------------------------------------

    event = BaseEvent(
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        subject_id="household-1",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    # --------------------------------------------------
    # Publish
    # --------------------------------------------------

    await publisher.publish(event)

    # --------------------------------------------------
    # Timeline assertions
    # --------------------------------------------------

    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == (
        event.subject_id
    )

    assert entry.event_type == (
        event.event_type
    )

    assert entry.event_name == (
        event.event_name
    )

    assert entry.state == (
        event.state
    )

    assert entry.description == (
        event.description
    )

    assert entry.resource_id == (
        event.resource_id
    )

    assert entry.resource_type == (
        event.resource_type
    )

    assert entry.created_at == (
        event.created_at
    )


@pytest.mark.asyncio
async def test_timeline_records_multiple_events_for_subject():

    publisher = EventPublisher()

    repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=repository,
    )

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    publisher.subscribe(
        timeline_listener,
    )

    prediction_event = BaseEvent(
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        subject_id="household-1",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    outcome_event = BaseEvent(
        event_type="outcome",
        event_name="outcome_recorded",
        state="observed",
        description="Outcome recorded",
        subject_id="household-1",
        resource_id="outcome-1",
        resource_type="outcome",
    )

    await publisher.publish(
        prediction_event,
    )

    await publisher.publish(
        outcome_event,
    )

    timeline = (
        await timeline_service.get_by_subject(
            "household-1",
        )
    )

    assert len(timeline) == 2

    assert timeline[0].event_name == (
        "prediction_created"
    )

    assert timeline[1].event_name == (
        "outcome_recorded"
    )


@pytest.mark.asyncio
async def test_event_publisher_notifies_timeline_listener():

    repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=repository,
    )

    listener = TimelineListener(
        service=timeline_service,
    )

    publisher = EventPublisher()

    publisher.subscribe(
        listener,
    )

    event = BaseEvent(
        subject_id="subject-123",
        event_type="conversation",
        event_name="message_received",
        state="completed",
        description="User reported scratching in the kitchen.",
        resource_id=None,
        resource_type=None,
    )

    await publisher.publish(event)

    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == "subject-123"
    assert entry.event_type == "conversation"
    assert entry.event_name == "message_received"
    assert entry.description == (
        "User reported scratching in the kitchen."
    )


@pytest.mark.asyncio
async def test_event_publisher_notifies_timeline_listener_new():

    repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=repository,
    )

    listener = TimelineListener(
        service=timeline_service,
    )

    publisher = EventPublisher()

    publisher.subscribe(
        listener,
    )

    event = BaseEvent(
        event_type="conversation",
        event_name="message_received",
        state="observed",
        description=(
            "I found droppings in my kitchen."
        ),
        subject_id="subject-123",
        resource_id="conversation-123",
        resource_type="conversation",
    )

    await publisher.publish(
        event,
    )

    entries = await repository.get_by_subject(
        "subject-123",
    )

    assert len(entries) == 1

    entry = entries[0]

    assert entry.event_type == "conversation"
    assert entry.event_name == "message_received"
    assert entry.subject_id == "subject-123"
    assert entry.resource_id == "conversation-123"
    assert entry.resource_type == "conversation"
    assert entry.description == (
        "I found droppings in my kitchen."
    )

@pytest.mark.asyncio
async def test_event_publisher_records_event_in_timeline_and_audit():

    publisher = EventPublisher()

    # Timeline
    timeline_repository = FakeTimelineRepository()
    timeline_service = TimelineService(
        repository=timeline_repository,
    )
    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    # Audit
    audit_repository = FakeAuditRepository()
    audit_service = AuditService(
        audit_repository=audit_repository,
    )
    audit_listener = AuditListener(
        audit_service=audit_service,
    )

    # Subscribe both
    publisher.subscribe(timeline_listener)
    publisher.subscribe(audit_listener)

    event = BaseEvent(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
    )

    await publisher.publish(event)

    # Timeline received it
    assert len(timeline_repository.entries) == 1

    timeline_entry = timeline_repository.entries[0]

    assert timeline_entry.event_name == "consent_granted"
    assert timeline_entry.subject_id == "household-1"

    # Audit received the same event
    assert len(audit_repository.records) == 1

    audit_record = audit_repository.records[0]

    assert audit_record.event_name == "consent_granted"
    assert audit_record.subject_id == "household-1"