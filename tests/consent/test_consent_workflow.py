from datetime import datetime, timezone

import pytest

from hios.capabilities.consent.models.consent import (
    Consent,
    ConsentPurpose,
)
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


@pytest.mark.asyncio
async def test_consent_workflow_grants_and_saves_consent():
    repository = FakeConsentRepository()
    service = ConsentService()

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
    )

    result = await workflow.grant(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert result.subject_id == "household-1"
    assert result.purpose == ConsentPurpose.PREDICTION
    assert result.granted is True
    assert result.granted_at is not None

    assert len(repository.saved) == 1
    assert repository.saved[0] is result


@pytest.mark.asyncio
async def test_consent_workflow_revokes_and_saves_consent():
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

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
    )

    result = await workflow.revoke(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert result is existing_consent
    assert result.granted is False
    assert result.revoked_at is not None

    assert len(repository.saved) == 1
    assert repository.saved[0] is result


@pytest.mark.asyncio
async def test_consent_workflow_revoke_returns_none_when_consent_does_not_exist():
    repository = FakeConsentRepository()
    service = ConsentService()

    workflow = ConsentWorkflow(
        consent_service=service,
        consent_repository=repository,
    )

    result = await workflow.revoke(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert result is None
    assert repository.saved == []