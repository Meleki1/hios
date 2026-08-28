import pytest

from hios.core.audit.models.audit_record import AuditRecord
from hios.core.audit.audit_service import AuditService
from tests.audit.fakes.fake_audit_repository import FakeAuditRepository


@pytest.mark.asyncio
async def test_audit_service_records_audit():

    repository = FakeAuditRepository()
    service = AuditService(repository)

    audit_record = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
        details={
            "purpose": "prediction",
        },
    )

    result = await service.record(
        audit_record,
    )

    assert result == audit_record
    assert len(repository.records) == 1
    assert repository.records[0] == audit_record


@pytest.mark.asyncio
async def test_audit_service_gets_by_id():

    repository = FakeAuditRepository()
    service = AuditService(repository)

    audit_record = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
    )

    await repository.save(audit_record)

    result = await service.get_by_id(
        audit_record.id,
    )

    assert result == audit_record

@pytest.mark.asyncio
async def test_audit_service_gets_by_subject():

    repository = FakeAuditRepository()
    service = AuditService(repository)

    first = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
    )

    second = AuditRecord(
        event_type="home",
        event_name="home_created",
        state="created",
        description="Home created successfully",
        subject_id="household-1",
    )

    other = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-2",
    )

    await repository.save(first)
    await repository.save(second)
    await repository.save(other)

    results = await service.get_by_subject(
        "household-1",
    )

    assert len(results) == 2
    assert first in results
    assert second in results
    assert other not in results

@pytest.mark.asyncio
async def test_audit_service_gets_by_resource():

    repository = FakeAuditRepository()
    service = AuditService(repository)

    first = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
    )

    second = AuditRecord(
        event_type="consent",
        event_name="consent_revoked",
        state="revoked",
        description="Consent revoked",
        subject_id="household-1",
        resource_id="consent-1",
        resource_type="consent",
    )

    other = AuditRecord(
        event_type="consent",
        event_name="consent_granted",
        state="granted",
        description="Consent granted",
        subject_id="household-1",
        resource_id="consent-2",
        resource_type="consent",
    )

    await repository.save(first)
    await repository.save(second)
    await repository.save(other)

    results = await service.get_by_resource(
        "consent-1",
    )

    assert len(results) == 2
    assert first in results
    assert second in results
    assert other not in results

