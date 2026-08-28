from hios.capabilities.consent.postgres.models.consent_record import (
    ConsentRecord,
)


def test_consent_record_has_expected_table():
    assert ConsentRecord.__tablename__ == "consents"


def test_consent_record_has_expected_columns():
    columns = {
        column.name
        for column in ConsentRecord.__table__.columns
    }

    assert columns == {
        "id",
        "subject_id",
        "purpose",
        "granted",
        "granted_at",
        "revoked_at",
    }