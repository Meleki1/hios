import pytest

from hios.capabilities.intelligence.collectors.environmental import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_environmental_signals_are_created():

    collector = EnvironmentalSignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        observations={
            "rainfall": "42mm",
            "temperature": "18C",
            "humidity": "82%",
        },
    )

    assert len(signals) == 3

    assert signals[0].type == SignalType.ENVIRONMENTAL
    assert signals[0].source == SignalSource.WEATHER

    assert signals[0].name == "rainfall"
    assert signals[0].value == "42mm"