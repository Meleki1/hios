import httpx
import pytest

from hios.capabilities.local_activity.clients.planning_data_http_client import (
    PlanningDataHTTPClient,
)

from hios.capabilities.local_activity.geo.query_builder import (
    GeoQueryBuilder,
)

from hios.capabilities.local_activity.mappers.planning_application_mapper import (
    PlanningApplicationMapper,
)

from hios.capabilities.local_activity.providers.planning_activity_provider import (
    PlanningActivityProvider,
)

from hios.capabilities.local_activity.providers.planning_application_adapter import (
    PlanningApplicationAdapter,
)


@pytest.mark.asyncio
async def test_planning_activity_provider_collects_and_maps_api_data():

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:

        return httpx.Response(
            200,
            json={
                "entities": [
                    {
                        "reference": "PA-001",
                        "category": "restaurant",
                        "status": "approved",
                        "description": (
                            "New restaurant development"
                        ),
                        "latitude": "51.5074",
                        "longitude": "-0.1278",
                        "observed_at": (
                            "2026-08-10T12:00:00+00:00"
                        ),
                        "source": (
                            "planning_authority"
                        ),
                        "source_url": (
                            "https://example.gov.uk/PA-001"
                        ),
                        "metadata": {
                            "development_type": (
                                "restaurant"
                            ),
                        },
                    }
                ]
            },
        )

    transport = httpx.MockTransport(
        handler,
    )

    async with httpx.AsyncClient(
        transport=transport,
    ) as client:

        provider = PlanningActivityProvider(
            client=PlanningDataHTTPClient(
                client=client,
            ),
            geo_query_builder=GeoQueryBuilder(),
            adapter=PlanningApplicationAdapter(),
            mapper=PlanningApplicationMapper(),
        )

        events = await provider.get_events(
            latitude=51.5074,
            longitude=-0.1278,
            radius_km=5.0,
        )

    assert len(events) == 1

    event = events[0]

    assert event.event_type == (
        "planning_application"
    )

    assert event.category == "restaurant"

    assert event.status == "approved"

    assert event.source == (
        "planning_authority"
    )

    assert event.source_reference == "PA-001"

    assert event.metadata[
        "development_type"
    ] == "restaurant"

    assert event.latitude == pytest.approx(
        51.5074
    )

    assert event.longitude == pytest.approx(
        -0.1278
    )