import pytest

from hios.core.audit.models.audit_record import AuditRecord
from hios.core.audit.postgres.audit_repository import (
    PostgresAuditRepository,
)


@pytest.mark.asyncio
async def test_audit_repository_saves_record(session):

    repository = PostgresAuditRepository(session)

    audit_record = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-123",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    result = await repository.save(audit_record)

    assert result.id == audit_record.id
    assert result.event_type == "consent"
    assert result.event_name == "consent_granted"
    assert result.subject_id == "household-1"


@pytest.mark.asyncio
async def test_audit_repository_gets_all(session):

    repository = PostgresAuditRepository(session)

    first = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
        details={"purpose": "prediction"},
    )

    second = AuditRecord(
        event_type="consent",
        event_name="consent_revoked",
        state="revoked",
        description="Consent revoked",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
        details={"purpose": "prediction"},
    )

    await repository.save(first)
    await repository.save(second)

    records = await repository.get_all()

    assert len(records) == 2


@pytest.mark.asyncio
async def test_audit_repository_gets_by_id(session):

    repository = PostgresAuditRepository(session)

    audit_record = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-2",
        resource_id="consent-2",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    await repository.save(audit_record)

    result = await repository.get_by_id(
        audit_record.id,
    )

    assert result is not None
    assert result.id == audit_record.id
    assert result.event_type == "consent"
    assert result.event_name == "consent_granted"
    assert result.subject_id == "household-2"


@pytest.mark.asyncio
async def test_audit_repository_get_by_id_returns_none_when_missing(
    session,
):

    repository = PostgresAuditRepository(session)

    result = await repository.get_by_id(
        "does-not-exist",
    )

    assert result is None


@pytest.mark.asyncio
async def test_audit_repository_gets_by_subject(session):

    repository = PostgresAuditRepository(session)

    first = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-3",
        resource_id="consent-3",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    second = AuditRecord(
        event_type="home",
        event_name="home_created",
        state="created",
        description="Home created successfully",
        subject_id="household-3",
        resource_id="home-3",
        resource_type="home",
        details={},
    )

    other_subject = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-4",
        resource_id="consent-4",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    await repository.save(first)
    await repository.save(second)
    await repository.save(other_subject)

    records = await repository.get_by_subject(
        "household-3",
    )

    record_ids = {record.id for record in records}

    assert first.id in record_ids
    assert second.id in record_ids
    assert other_subject.id not in record_ids

    assert len(records) == 2


@pytest.mark.asyncio
async def test_audit_repository_gets_by_resource(session):

    repository = PostgresAuditRepository(session)

    first = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-5",
        resource_id="consent-5",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    second = AuditRecord(
        event_type="consent",
        event_name="consent_revoked",
        state="revoked",
        description="Consent revoked",
        subject_id="household-5",
        resource_id="consent-5",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    other_resource = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-5",
        resource_id="consent-6",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    await repository.save(first)
    await repository.save(second)
    await repository.save(other_resource)

    records = await repository.get_by_resource(
        "consent-5",
    )

    record_ids = {record.id for record in records}

    assert first.id in record_ids
    assert second.id in record_ids
    assert other_resource.id not in record_ids

    assert len(records) == 2