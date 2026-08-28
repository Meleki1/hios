from hios.capabilities.consent.models.consent import (
    ConsentPurpose,
)
from hios.capabilities.consent.consent_service import (
    ConsentService,
)


def test_consent_service_grants_consent():
    service = ConsentService()

    consent = service.grant(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert consent.id
    assert consent.subject_id == "household-1"
    assert consent.purpose == ConsentPurpose.PREDICTION
    assert consent.granted is True
    assert consent.granted_at is not None
    assert consent.revoked_at is None


def test_consent_service_revokes_consent():
    service = ConsentService()

    consent = service.grant(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    revoked = service.revoke(consent)

    assert revoked is consent
    assert revoked.granted is False
    assert revoked.revoked_at is not None