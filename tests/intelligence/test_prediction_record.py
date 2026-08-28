from hios.capabilities.intelligence.postgres.models.prediction import (
    PredictionRecord,
)
from hios.db.base import Base


def test_prediction_record_uses_shared_base():

    assert issubclass(
        PredictionRecord,
        Base,
    )


def test_prediction_record_table_name():

    assert PredictionRecord.__tablename__ == (
        "intelligence_predictions"
    )


def test_prediction_record_has_expected_columns():

    columns = PredictionRecord.__table__.columns

    assert "id" in columns
    assert "subject_id" in columns
    assert "target" in columns
    assert "horizon_days" in columns
    assert "probability" in columns
    assert "confidence" in columns
    assert "evidence" in columns
    assert "intent_score" in columns