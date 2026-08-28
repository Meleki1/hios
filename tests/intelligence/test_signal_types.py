from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.models.signal import Signal



def test_image_is_a_signal_source():
    assert SignalSource.IMAGE.value == "image"


def test_image_is_a_signal_type():
    assert SignalType.IMAGE.value == "image"


def test_signal_source_image_is_distinct_from_signal_type():
    assert SignalSource.IMAGE != SignalSource.HOME_ASSIST
    assert SignalType.IMAGE != SignalType.CONVERSATION



def test_signal_can_represent_an_image_observation():
    signal = Signal(
        type=SignalType.IMAGE,
        source=SignalSource.IMAGE,
        name="possible_pest_evidence",
        value="Possible rodent evidence detected in kitchen",
        strength=0.91,
        confidence=0.91,
        metadata={
            "location": "kitchen",
            "category": "pest",
        },
    )

    assert signal.type is SignalType.IMAGE
    assert signal.source is SignalSource.IMAGE
    assert signal.name == "possible_pest_evidence"
    assert signal.value == (
        "Possible rodent evidence detected in kitchen"
    )
    assert signal.confidence == 0.91