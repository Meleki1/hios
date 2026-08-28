import pytest

from hios.capabilities.environmental.providers.mock import MockEnvironmentalProvider
from hios.capabilities.environmental.service import EnvironmentalService
from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation

@pytest.mark.asyncio
async def test_environmental_service_delegates_to_provider():

    provider = MockEnvironmentalProvider()

    service = EnvironmentalService(
        provider=provider,
    )

    observation = await service.get_observation(
        latitude=51.5074,
        longitude=-0.1278,
    )

    assert observation is not None

    assert observation.rainfall_mm == 42.0
    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78.0
    assert observation.wind_speed_mps == 4.2
    assert observation.frost is False

def test_environmental_service_converts_observation_to_observations():

    service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    observations = service.to_observations(
        observation,
    )

    assert observations == {
        "rainfall_mm": "42.0",
        "temperature_c": "18.5",
        "humidity_percent": "78.0",
        "wind_speed_mps": "4.2",
        "frost": "False",
    }