from hios.capabilities.intelligence.postgres.models.prediction_evaluation import (
    PredictionEvaluationRecord,
)
from hios.db.base import Base


def test_prediction_evaluation_record_uses_shared_base():

    assert issubclass(
        PredictionEvaluationRecord,
        Base,
    )


def test_prediction_evaluation_record_table_name():

    assert PredictionEvaluationRecord.__tablename__ == (
        "intelligence_prediction_evaluations"
    )


def test_prediction_evaluation_record_has_expected_columns():

    columns = PredictionEvaluationRecord.__table__.columns

    assert "id" in columns
    assert "prediction_id" in columns
    assert "outcome_id" in columns
    assert "correct" in columns
    assert "details" in columns