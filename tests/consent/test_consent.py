from datetime import datetime, timezone

from hios.capabilities.consent.models.consent import (
    Consent,
    ConsentPurpose,
)


def test_consent_can_be_created():
    granted_at = datetime.now(timezone.utc)

    consent = Consent(
        id="consent-1",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
        granted=True,
        granted_at=granted_at,
    )

    assert consent.id == "consent-1"
    assert consent.subject_id == "household-1"
    assert consent.purpose == ConsentPurpose.PREDICTION
    assert consent.granted is True
    assert consent.granted_at == granted_at
    assert consent.revoked_at is None


def test_consent_can_be_revoked():
    granted_at = datetime.now(timezone.utc)
    revoked_at = datetime.now(timezone.utc)

    consent = Consent(
        id="consent-1",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
        granted=True,
        granted_at=granted_at,
        revoked_at=revoked_at,
    )

    assert consent.granted is True
    assert consent.revoked_at == revoked_at


def test_consent_purpose_values():
    assert ConsentPurpose.PREDICTION.value == "prediction"
    assert ConsentPurpose.TIMELINE.value == "timeline"
    assert ConsentPurpose.PERSONALIZATION.value == "personalization"
    assert ConsentPurpose.BUSINESS_SHARING.value == "business_sharing"