import pytest

from hios.capabilities.consent.models.consent import (
    ConsentPurpose,
)
from hios.capabilities.consent.postgres.repository.consent_repository import (
    PostgresConsentRepository,
)
from hios.capabilities.consent.postgres.models.consent_record import (
    ConsentRecord,
)


def make_consent():
    from datetime import datetime, timezone

    from hios.capabilities.consent.models.consent import Consent

    return Consent(
        id="consent-1",
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
        granted=True,
        granted_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_consent_repository_saves_record(session):
    await session.execute(
        ConsentRecord.__table__.delete()
    )
    await session.commit()

    repository = PostgresConsentRepository(session)

    consent = make_consent()

    result = await repository.save(consent)

    assert result.id == consent.id
    assert result.subject_id == "household-1"
    assert result.purpose == ConsentPurpose.PREDICTION
    assert result.granted is True

@pytest.mark.asyncio
async def test_consent_repository_gets_all(session):
    await session.execute(
        ConsentRecord.__table__.delete()
    )
    await session.commit()

    repository = PostgresConsentRepository(session)

    consent = make_consent()

    await repository.save(consent)

    results = await repository.get_all()

    assert len(results) == 1

    result = results[0]

    assert result.id == consent.id
    assert result.subject_id == "household-1"
    assert result.purpose == ConsentPurpose.PREDICTION
    assert result.granted is True

@pytest.mark.asyncio
async def test_consent_repository_gets_by_subject_and_purpose(session):
    await session.execute(
        ConsentRecord.__table__.delete()
    )
    await session.commit()

    repository = PostgresConsentRepository(session)

    consent = make_consent()

    await repository.save(consent)

    result = await repository.get(
        subject_id="household-1",
        purpose=ConsentPurpose.PREDICTION,
    )

    assert result is not None
    assert result.id == consent.id
    assert result.subject_id == "household-1"
    assert result.purpose == ConsentPurpose.PREDICTION
    assert result.granted is True

@pytest.mark.asyncio
async def test_consent_repository_returns_none_when_not_found(session):
    await session.execute(
        ConsentRecord.__table__.delete()
    )
    await session.commit()

    repository = PostgresConsentRepository(session)

    result = await repository.get(
        subject_id="household-1",
        purpose=ConsentPurpose.BUSINESS_SHARING,
    )

    assert result is None