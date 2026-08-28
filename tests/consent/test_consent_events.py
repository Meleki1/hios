import pytest
from datetime import datetime, timezone
from hios.capabilities.consent.models.consent import ConsentPurpose, Consent
from hios.core.events.consent_events import ConsentGrantedEvent, ConsentRevokedEvent
from hios.capabilities.consent.consent_service import ConsentService
from hios.capabilities.consent.consent_workflow import ConsentWorkflow



class FakeConsentRepository:

    def __init__(self, consent=None):
        self.consent = consent
        self.saved = []

    async def save(self, consent):
        self.saved.append(consent)
        self.consent = consent
        return consent

    async def get(self, subject_id, purpose):
        if self.consent is None:
            return None

        if (
            self.consent.subject_id == subject_id
            and self.consent.purpose == purpose
        ):
            return self.consent

        return None

class FakeEventPublisher:

    def __init__(self):
        self.events = []

    async def publish(self, event):
        self.events.append(event)

def test_consent_granted_event_has_expected_values():
    event = ConsentGrantedEvent(
        consent_id="consent-123",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert event.event_type == "consent"
    assert event.event_name == "consent_granted"
    assert event.state == "granted"
    assert event.description == "Consent granted"

    assert event.subject_id == "household-1"
    assert event.resource_id == "consent-123"
    assert event.resource_type == "consent"

    assert event.purpose == ConsentPurpose.PREDICTION
    assert event.created_at is not None

def test_consent_revoked_event_has_expected_values():
    event = ConsentRevokedEvent(
        consent_id="consent-123",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert event.event_type == "consent"
    assert event.event_name == "consent_revoked"
    assert event.state == "revoked"
    assert event.description == "Consent revoked"

    assert event.subject_id == "household-1"
    assert event.resource_id == "consent-123"
    assert event.resource_type == "consent"

    assert event.purpose == ConsentPurpose.PREDICTION
    assert event.created_at is not None

@pytest.mark.asyncio
async def test_consent_workflow_publishes_granted_event():
    repository = FakeConsentRepository()
    service = ConsentService()
    publisher = FakeEventPublisher()

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
        event_publisher=publisher,
    )

    result = await workflow.grant(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert len(publisher.events) == 1

    event = publisher.events[0]

    assert event.event_type == "consent"
    assert event.event_name == "consent_granted"
    assert event.state == "granted"
    assert event.subject_id == "household-1"
    assert event.resource_id == result.id
    assert event.resource_type == "consent"
    assert event.purpose == ConsentPurpose.PREDICTION

@pytest.mark.asyncio
async def test_consent_workflow_publishes_revoked_event():
    existing_consent = Consent(
        id="consent-1",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
        granted=True,
        granted_at=datetime.now(timezone.utc),
    )

    repository = FakeConsentRepository(
        consent=existing_consent,
    )
    service = ConsentService()
    publisher = FakeEventPublisher()

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
        event_publisher=publisher,
    )

    result = await workflow.revoke(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert len(publisher.events) == 1

    event = publisher.events[0]

    assert event.event_type == "consent"
    assert event.event_name == "consent_revoked"
    assert event.state == "revoked"
    assert event.subject_id == "household-1"
    assert event.resource_id == result.id
    assert event.resource_type == "consent"
    assert event.purpose == ConsentPurpose.PREDICTION

@pytest.mark.asyncio
async def test_consent_workflow_does_not_publish_event_when_revoke_target_is_missing():
    repository = FakeConsentRepository()
    service = ConsentService()
    publisher = FakeEventPublisher()

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
        event_publisher=publisher,
    )

    result = await workflow.revoke(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert result is None
    assert publisher.events == []