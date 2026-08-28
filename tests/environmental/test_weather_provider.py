import pytest

from hios.capabilities.environmental.providers.weather import (
    WeatherProvider,
)


class FakeWeatherClient:

    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:

        return {
            "current": {
                "temperature_2m": 18.5,
                "relative_humidity_2m": 78,
                "precipitation": 42.0,
                "wind_speed_10m": 4.2,
            }
        }


@pytest.mark.asyncio
async def test_weather_provider_maps_weather_response():

    provider = WeatherProvider(
        client=FakeWeatherClient(),
    )

    observation = await provider.get_observation(
        latitude=51.5074,
        longitude=-0.1278,
    )

    assert observation is not None

    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78
    assert observation.rainfall_mm == 42.0
    assert observation.wind_speed_mps == 4.2