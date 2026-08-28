import httpx
import pytest

from hios.capabilities.local_activity.clients.planning_data_http_client import (
    PlanningDataHTTPClient,
)


@pytest.mark.asyncio
async def test_planning_data_http_client_searches_planning_applications():

    captured = {}

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        captured["url"] = str(request.url)

        return httpx.Response(
            200,
            json={
                "entities": [
                    {
                        "entity": 123,
                        "reference": "PA-001",
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
            )
        )

        results = await planning_client.search(
            geometry=(
                "POLYGON((-0.15 51.50,"
                "-0.10 51.50,"
                "-0.10 51.52,"
                "-0.15 51.52,"
                "-0.15 51.50))"
            ),
            limit=100,
            offset=0,
        )

    assert len(results) == 1

    assert results[0]["entity"] == 123

    assert results[0]["reference"] == "PA-001"

    assert (
        "dataset=planning-application"
        in captured["url"]
    )

    assert (
        "geometry_relation=intersects"
        in captured["url"]
    )

@pytest.mark.asyncio
async def test_planning_data_http_client_collects_multiple_pages():

    requests = []

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        requests.append(request)

        offset = int(
            request.url.params["offset"]
        )

        if offset == 0:
            return httpx.Response(
                200,
                json={
                    "entities": [
                        {"reference": "PA-001"},
                        {"reference": "PA-002"},
                    ]
                },
            )

        return httpx.Response(
            200,
            json={
                "entities": [
                    {"reference": "PA-003"},
                ]
            },
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
            )
        )

        results = await planning_client.search(
            geometry=(
                "POLYGON((-0.15 51.50,"
                "-0.10 51.50,"
                "-0.10 51.52,"
                "-0.15 51.52,"
                "-0.15 51.50))"
            ),
            limit=2,
            max_pages=5,
        )

    assert len(results) == 3

    assert [
        item["reference"]
        for item in results
    ] == [
        "PA-001",
        "PA-002",
        "PA-003",
    ]

    assert len(requests) == 2

    assert requests[0].url.params[
        "offset"
    ] == "0"

    assert requests[1].url.params[
        "offset"
    ] == "2"


@pytest.mark.asyncio
async def test_planning_data_http_client_rejects_invalid_limit():

    async with httpx.AsyncClient() as http_client:

        planning_client = (
            PlanningDataHTTPClient(
                client=http_client,
            )
        )

        with pytest.raises(ValueError):

            await planning_client.search(
                geometry="POLYGON(...)",
                limit=0,
            )

@pytest.mark.asyncio
async def test_planning_data_http_client_rejects_invalid_max_pages():

    async with httpx.AsyncClient() as http_client:

        planning_client = (
            PlanningDataHTTPClient(
                client=http_client,
            )
        )

        with pytest.raises(ValueError):

            await planning_client.search(
                geometry="POLYGON(...)",
                max_pages=0,
            )

@pytest.mark.asyncio
async def test_planning_data_http_client_propagates_timeout():

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        raise httpx.ReadTimeout(
            "Planning API timed out",
            request=request,
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
        timeout=10.0,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
            )
        )

        with pytest.raises(
            httpx.ReadTimeout
        ):

            await planning_client.search(
                geometry=(
                    "POLYGON((-0.15 51.50,"
                    "-0.10 51.50,"
                    "-0.10 51.52,"
                    "-0.15 51.52,"
                    "-0.15 51.50))"
                )
            )

@pytest.mark.asyncio
async def test_planning_data_http_client_retries_server_error():

    attempts = 0

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        nonlocal attempts

        attempts += 1

        if attempts == 1:
            return httpx.Response(
                503,
                request=request,
            )

        return httpx.Response(
            200,
            json={
                "entities": [
                    {
                        "reference": "PA-001",
                    }
                ]
            },
            request=request,
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
                max_retries=2,
            )
        )

        results = await planning_client.search(
            geometry="POLYGON(...)",
        )

    assert attempts == 2

    assert results[0]["reference"] == (
        "PA-001"
    )

@pytest.mark.asyncio
async def test_planning_data_http_client_stops_after_max_retries():

    attempts = 0

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        nonlocal attempts

        attempts += 1

        return httpx.Response(
            503,
            request=request,
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
                max_retries=2,
            )
        )

        with pytest.raises(
            httpx.HTTPStatusError
        ):

            await planning_client.search(
                geometry="POLYGON(...)",
            )

    assert attempts == 3


@pytest.mark.asyncio
async def test_planning_data_http_client_does_not_retry_client_error():

    attempts = 0

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        nonlocal attempts

        attempts += 1

        return httpx.Response(
            400,
            request=request,
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
                max_retries=2,
            )
        )

        with pytest.raises(
            httpx.HTTPStatusError
        ):

            await planning_client.search(
                geometry="POLYGON(...)",
            )

    assert attempts == 1

@pytest.mark.asyncio
async def test_planning_data_http_client_does_not_retry_client_error():

    attempts = 0

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        nonlocal attempts

        attempts += 1

        return httpx.Response(
            400,
            request=request,
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        planning_client = (
            PlanningDataHTTPClient(
                client=client,
                max_retries=2,
            )
        )

        with pytest.raises(
            httpx.HTTPStatusError
        ):

            await planning_client.search(
                geometry="POLYGON(...)",
            )

    assert attempts == 1
