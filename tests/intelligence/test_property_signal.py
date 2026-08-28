import pytest

from hios.capabilities.intelligence.collectors.property import (
    PropertySignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_property_characteristics_become_signals():

    collector = PropertySignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        characteristics={
            "property_type": "detached",
            "has_loft": "true",
            "near_woodland": "true",
        },
    )

    assert len(signals) == 3

    assert all(
        signal.type == SignalType.PROPERTY
        for signal in signals
    )

    assert signals[0].name == "property_type"
    assert signals[0].value == "detached"

    assert signals[1].name == "has_loft"
    assert signals[1].value == "true"