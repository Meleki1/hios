import pytest
from pydantic import ValidationError

from hios.capabilities.intelligence.models.signal import (
    Signal,
    SignalSource,
    SignalType,
)


def test_signal_defaults_are_valid():

    signal = Signal(
        type=SignalType.LOCAL_ACTIVITY,
        source=SignalSource.LOCAL_ACTIVITY,
        name="restaurant_development",
        value="increasing",
    )

    assert signal.strength == 1.0
    assert signal.confidence == 1.0
    assert signal.id is not None
    assert signal.observed_at is not None
    assert signal.metadata == {}


def test_signal_accepts_explicit_strength_and_confidence():

    signal = Signal(
        type=SignalType.ENVIRONMENTAL,
        source=SignalSource.WEATHER,
        name="rainfall",
        value="heavy",
        strength=0.7,
        confidence=0.9,
    )

    assert signal.strength == 0.7
    assert signal.confidence == 0.9

def test_signal_rejects_strength_above_one():

    with pytest.raises(ValidationError):

        Signal(
            type=SignalType.LOCAL_ACTIVITY,
            source=SignalSource.LOCAL_ACTIVITY,
            name="restaurant_development",
            value="increasing",
            strength=1.1,
        )


def test_signal_rejects_negative_confidence():

    with pytest.raises(ValidationError):

        Signal(
            type=SignalType.LOCAL_ACTIVITY,
            source=SignalSource.LOCAL_ACTIVITY,
            name="restaurant_development",
            value="increasing",
            confidence=-0.1,
        )