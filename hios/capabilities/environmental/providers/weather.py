from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.providers.base import (
    EnvironmentalProvider,
)
from hios.capabilities.environmental.providers.weather_client import (
    WeatherHttpClient,
)


class WeatherProvider(EnvironmentalProvider):

    def __init__(
        self,
        client: WeatherHttpClient,
    ):
        self._client = client

    async def get_observation(
        self,
        latitude: float,
        longitude: float,
    ) -> EnvironmentalObservation | None:

        data = await self._client.get_current_weather(
            latitude=latitude,
            longitude=longitude,
        )

        current = data.get("current")

        if not current:
            return None

        return EnvironmentalObservation(
            rainfall_mm=current.get(
                "precipitation"
            ),
            temperature_c=current.get(
                "temperature_2m"
            ),
            humidity_percent=current.get(
                "relative_humidity_2m"
            ),
            wind_speed_mps=current.get(
                "wind_speed_10m"
            ),
        )