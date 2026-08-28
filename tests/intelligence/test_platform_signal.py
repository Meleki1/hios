import pytest

from hios.capabilities.intelligence.collectors.platform import (
    PlatformBehaviourSignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_platform_behaviour_becomes_signals():

    collector = PlatformBehaviourSignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        behaviours={
            "return_visits": "3",
            "saved_advice": "true",
            "price_comparisons": "2",
        },
    )

    assert len(signals) == 3

    assert all(
        signal.type == SignalType.PLATFORM_BEHAVIOUR
        for signal in signals
    )

    assert signals[0].name == "return_visits"
    assert signals[0].value == "3"

    assert signals[1].name == "saved_advice"
    assert signals[1].value == "true"