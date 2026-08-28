import pytest

from hios.capabilities.environmental.providers.mock import (
    MockEnvironmentalProvider,
)


@pytest.mark.asyncio
async def test_mock_environmental_provider_returns_observation():

    provider = MockEnvironmentalProvider()

    observation = await provider.get_observation(
        latitude=51.5074,
        longitude=-0.1278,
    )

    assert observation is not None

    assert observation.rainfall_mm == 42.0
    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78.0
    assert observation.wind_speed_mps == 4.2
    assert observation.frost is False