from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.postgres.models.prediction_evaluation import (
    PredictionEvaluationRecord,
)
from hios.capabilities.intelligence.postgres.prediction_evaluation_repository import (
    PostgresPredictionEvaluationRepository,
)


def test_evaluation_record_maps_to_domain():

    record = PredictionEvaluationRecord(
        id="evaluation-1",
        prediction_id="prediction-1",
        outcome_id="outcome-1",
        correct=True,
        details={
            "reason": "event_occurred",
        },
    )

    evaluation = (
        PostgresPredictionEvaluationRepository._to_domain(
            record,
        )
    )

    assert isinstance(
        evaluation,
        PredictionEvaluation,
    )

    assert evaluation.id == "evaluation-1"
    assert evaluation.prediction_id == "prediction-1"
    assert evaluation.outcome_id == "outcome-1"
    assert evaluation.correct is True
    assert evaluation.details == {
        "reason": "event_occurred",
    }