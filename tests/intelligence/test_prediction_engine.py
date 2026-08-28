import pytest

from hios.capabilities.intelligence.basic_prediction_engine import (
    BasicPredictionEngine,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)

from hios.capabilities.intelligence.models.prediction import Prediction


@pytest.mark.asyncio
async def test_prediction_preserves_intent_evidence():

    signal = Signal(
        type=SignalType.EXPLICIT_INTENT,
        source=SignalSource.HOME_ASSIST,
        name="intent",
        value="asked_for_price",
    )

    intent_score = IntentScore(
        score=40.0,
        level=IntentLevel.MEDIUM,
        confidence=1.0,
        signals=[signal],
    )

    engine = BasicPredictionEngine()

    prediction = await engine.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        intent_score=intent_score,
    )

    assert prediction.subject_id == "household-1"
    assert prediction.target == "pest_control_need"
    assert prediction.horizon_days == 90

    assert prediction.intent_score.score == 40.0

    assert prediction.probability is None

    assert prediction.evidence == [
        "asked_for_price"
    ]

def test_prediction_has_unique_id():

    prediction = Prediction(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        intent_score=IntentScore(
            score=40.0,
            level=IntentLevel.MEDIUM,
        ),
    )

    assert prediction.id
    assert isinstance(prediction.id, str)