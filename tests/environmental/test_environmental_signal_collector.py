import pytest

from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.signal_collector import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_environmental_signal_collector_collects_available_observations():

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    collector = EnvironmentalSignalCollector()

    signals = await collector.collect(
        observation,
    )

    assert len(signals) == 5

    assert all(
        signal.type == SignalType.ENVIRONMENTAL
        for signal in signals
    )

    values = {
        signal.name
        for signal in signals
    }

    assert "rainfall" in values
    assert "temperature" in values
    assert "humidity" in values
    assert "wind_speed" in values
    assert "frost" in values