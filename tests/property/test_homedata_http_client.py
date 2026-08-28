import httpx
import pytest

from hios.capabilities.property.providers.homedata_http import (
    HttpHomedataClient,
)


@pytest.mark.asyncio
async def test_homedata_http_client_gets_property():

    captured = {}

    async def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured["url"] = str(request.url)
        captured["authorization"] = (
            request.headers["Authorization"]
        )

        return httpx.Response(
            200,
            json={
                "uprn": 100023336956,
                "full_address": (
                    "10 Example Road, London"
                ),
                "postcode": "SW1A 1AA",
                "construction_age_band": (
                    "1890-1918"
                ),
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        homedata = HttpHomedataClient(
            api_key="test-api-key",
            client=client,
        )

        result = await homedata.get_property(
            "100023336956",
        )

    assert result["uprn"] == 100023336956

    assert captured["url"] == (
        "https://api.homedata.co.uk/api"
        "/property/100023336956/base"
    )

    assert captured["authorization"] == (
        "Api-Key test-api-key"
    )