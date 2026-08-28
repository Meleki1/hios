import pytest

from hios.core.audit.audit_listener import AuditListener
from hios.core.audit.models.audit_record import AuditRecord
from hios.core.events.base_event import BaseEvent


class FakeAuditService:

    def __init__(self):
        self.records: list[AuditRecord] = []

    async def record(
        self,
        audit_record: AuditRecord,
    ) -> AuditRecord:

        self.records.append(audit_record)

        return audit_record


@pytest.mark.asyncio
async def test_audit_listener_records_event():

    audit_service = FakeAuditService()

    listener = AuditListener(
        audit_service,
    )

    event = BaseEvent(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
    )

    await listener.listen(event)

    assert len(audit_service.records) == 1

    record = audit_service.records[0]

    assert record.event_type == event.event_type
    assert record.event_name == event.event_name
    assert record.state == event.state
    assert record.description == event.description
    assert record.subject_id == event.subject_id
    assert record.resource_id == event.resource_id
    assert record.resource_type == event.resource_type
    assert record.occurred_at == event.created_at
    

from hios.core.events.event_publisher import EventPublisher


@pytest.mark.asyncio
async def test_event_publisher_delivers_event_to_audit_listener():

    audit_service = FakeAuditService()

    listener = AuditListener(
        audit_service,
    )

    publisher = EventPublisher()

    publisher.subscribe(listener)

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

    assert len(audit_service.records) == 1

    record = audit_service.records[0]

    assert record.event_name == "consent_granted"
    assert record.state == "granted"
    assert record.subject_id == "household-1"
    assert record.resource_id == "consent-1"

    