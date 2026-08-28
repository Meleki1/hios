from hios.capabilities.intelligence.postgres.models.outcome import (
    OutcomeRecord,
)
from hios.db.base import Base


def test_outcome_record_uses_shared_base():

    assert issubclass(
        OutcomeRecord,
        Base,
    )


def test_outcome_record_table_name():

    assert OutcomeRecord.__tablename__ == (
        "intelligence_outcomes"
    )


def test_outcome_record_has_expected_columns():

    columns = OutcomeRecord.__table__.columns

    assert "id" in columns
    assert "prediction_id" in columns
    assert "subject_id" in columns
    assert "target" in columns
    assert "occurred" in columns
    assert "observed_at" in columns
    assert "details" in columns