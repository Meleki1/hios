from datetime import datetime, timezone

from hios.core.audit.models.audit_record import AuditRecord


def test_audit_record_has_expected_values():
    record = AuditRecord(
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

    assert record.id is not None

    assert record.event_type == "consent"
    assert record.event_name == "consent_granted"
    assert record.state == "granted"
    assert record.description == "Consent granted"

    assert record.subject_id == "household-1"
    assert record.resource_id == "consent-123"
    assert record.resource_type == "consent"

    assert record.details == {
        "purpose": "prediction",
    }

    assert record.occurred_at is not None
    assert record.occurred_at.tzinfo is not None
    assert record.occurred_at.utcoffset() == timezone.utc.utcoffset(
        record.occurred_at
    )


def test_audit_record_generates_id_and_timestamp():
    before = datetime.now(timezone.utc)

    record = AuditRecord(
        event_type="home",
        event_name="home_created",
        state="created",
        description="Home created successfully",
        subject_id="household-1",
    )

    after = datetime.now(timezone.utc)

    assert record.id is not None
    assert record.occurred_at >= before
    assert record.occurred_at <= after


def test_audit_record_defaults_optional_fields_and_details():
    record = AuditRecord(
        event_type="conversation",
        event_name="message_received",
        state="observed",
        description="Conversation message observed",
        subject_id="household-1",
    )

    assert record.resource_id is None
    assert record.resource_type is None
    assert record.details == {}


from hios.core.audit.postgres.models.audit_record import AuditRecord as AuditRecordModel
from hios.db.base import Base


def test_audit_record_has_expected_table():
    assert AuditRecordModel.__tablename__ == "audit_records"

    assert "audit_records" in Base.metadata.tables


def test_audit_record_has_expected_columns():
    table = AuditRecordModel.__table__

    expected_columns = {
        "id",
        "event_type",
        "event_name",
        "state",
        "description",
        "subject_id",
        "resource_id",
        "resource_type",
        "occurred_at",
        "details",
    }

    assert set(table.columns.keys()) == expected_columns


def test_audit_record_has_expected_primary_key():
    table = AuditRecordModel.__table__

    assert table.primary_key.columns.keys() == ["id"]


def test_audit_record_has_expected_indexes():
    table = AuditRecordModel.__table__

    index_columns = {
        tuple(column.name for column in index.columns)
        for index in table.indexes
    }

    assert ("event_type",) in index_columns
    assert ("event_name",) in index_columns
    assert ("subject_id",) in index_columns
    assert ("resource_id",) in index_columns
    assert ("occurred_at",) in index_columns