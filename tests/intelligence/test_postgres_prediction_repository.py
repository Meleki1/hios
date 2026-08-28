from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.postgres.models.prediction import (
    PredictionRecord,
)
from hios.capabilities.intelligence.postgres.prediction_repository import (
    PostgresPredictionRepository,
)


def test_prediction_record_maps_to_domain():

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    record = PredictionRecord(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        probability=None,
        confidence=1.0,
        evidence=[
            "asked_for_price",
        ],
        intent_score=intent_score.model_dump(
            mode="json",
        ),
    )

    prediction = PostgresPredictionRepository._to_domain(
        record,
    )

    assert isinstance(prediction, Prediction)

    assert prediction.id == "prediction-1"
    assert prediction.subject_id == "household-1"
    assert prediction.target == "pest_control_need"
    assert prediction.horizon_days == 90
    assert prediction.probability is None
    assert prediction.confidence == 1.0
    assert prediction.evidence == [
        "asked_for_price",
    ]

    assert prediction.intent_score.score == 70.0
    assert prediction.intent_score.level == IntentLevel.HIGH