from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)


def test_prediction_evaluation_can_be_created():

    evaluation = PredictionEvaluation(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        correct=True,
        details={
            "reason": "predicted_event_occurred",
        },
    )

    assert evaluation.prediction_id == "prediction-1"
    assert evaluation.outcome_id == "outcome-1"
    assert evaluation.correct is True
    assert evaluation.details["reason"] == (
        "predicted_event_occurred"
    )

def test_prediction_evaluation_has_unique_id():

    evaluation = PredictionEvaluation(
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        correct=True,
    )

    assert evaluation.id
    assert isinstance(evaluation.id, str)