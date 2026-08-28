import httpx
import pytest

from hios.capabilities.property.providers.homedata_address_http import (
    HttpHomedataAddressClient,
)


@pytest.mark.asyncio
async def test_homedata_address_http_client_searches_address():

    captured = {}

    async def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured["url"] = str(
            request.url
        )

        captured["authorization"] = (
            request.headers["Authorization"]
        )

        return httpx.Response(
            200,
            json={
                "suggestions": [
                    {
                        "uprn": 100023336956,
                        "address": (
                            "10 Example Road, London"
                        ),
                        "postcode": "SW1A 1AA",
                    }
                ],
                "meta": {
                    "total": 1,
                },
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        address_client = (
            HttpHomedataAddressClient(
                api_key="test-api-key",
                client=client,
            )
        )

        results = await address_client.search(
            "10 Example Road, London",
        )

    assert len(results) == 1

    assert results[0]["uprn"] == (
        100023336956
    )

    assert results[0]["address"] == (
        "10 Example Road, London"
    )

    assert captured["authorization"] == (
        "Api-Key test-api-key"
    )

    assert (
        "q=10+Example+Road%2C+London"
        in captured["url"]
    )