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


def test_intent_score_can_be_created():

    signal = Signal(
        type=SignalType.EXPLICIT_INTENT,
        source=SignalSource.HOME_ASSIST,
        name="asked_for_price",
        value="true",
    )

    result = IntentScore(
        score=40.0,
        level=IntentLevel.MEDIUM,
        confidence=0.9,
        signals=[signal],
    )

    assert result.score == 40.0
    assert result.level == IntentLevel.MEDIUM
    assert result.confidence == 0.9

    assert len(result.signals) == 1
    assert result.signals[0].name == "asked_for_price"



