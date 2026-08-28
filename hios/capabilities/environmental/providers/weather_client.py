from typing import Any

import httpx


class WeatherHttpClient:

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(
        self,
        timeout: float = 10.0,
        client: httpx.AsyncClient | None = None,
    ):
        self._timeout = timeout
        self._client = client

    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, Any]:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "wind_speed_10m"
            ),
        }

        if self._client is not None:
            response = await self._client.get(
                self.BASE_URL,
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()