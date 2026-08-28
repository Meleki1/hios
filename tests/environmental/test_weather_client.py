import httpx
import pytest

from hios.capabilities.environmental.providers.weather_client import (
    WeatherHttpClient,
)


@pytest.mark.asyncio
async def test_weather_http_client_gets_current_weather():

    captured = {}

    async def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured["url"] = str(request.url)

        return httpx.Response(
            200,
            json={
                "latitude": 51.5074,
                "longitude": -0.1278,
                "current": {
                    "temperature_2m": 18.5,
                    "relative_humidity_2m": 78,
                    "precipitation": 42.0,
                    "wind_speed_10m": 4.2,
                },
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        weather_client = WeatherHttpClient(
            client=client,
        )

        result = await weather_client.get_current_weather(
            latitude=51.5074,
            longitude=-0.1278,
        )

    assert result["current"]["temperature_2m"] == 18.5
    assert result["current"]["relative_humidity_2m"] == 78
    assert result["current"]["precipitation"] == 42.0
    assert result["current"]["wind_speed_10m"] == 4.2

    assert "latitude=51.5074" in captured["url"]
    assert "longitude=-0.1278" in captured["url"]