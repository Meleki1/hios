import pytest
from hios.capabilities.local_activity.local_activity_service import LocalActivityService
from hios.capabilities.local_activity.providers.planning_applications import MockPlanningApplicationProvider
from hios.capabilities.intelligence.collectors.local_activity import LocalActivitySignalCollector
from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.intelligence.models.signal_source import SignalSource
from hios.capabilities.intelligence.models.signal_type import SignalType


from hios.capabilities.local_activity.local_activity_provider import (
    LocalActivityProvider,
)


from hios.capabilities.local_activity.models.provider_result import (
    ProviderStatus,
)

class SuccessfulLocalActivityProvider(
    LocalActivityProvider
):

    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[LocalActivityEvent]:

        return [
            LocalActivityEvent(
                event_type="planning_application",
                category="restaurant",
                latitude=latitude,
                longitude=longitude,
                status="approved",
                source="planning_authority",
                source_reference="PA-001",
                metadata={
                    "development_type": "restaurant",
                },
            )
        ]


class FailingLocalActivityProvider(
    LocalActivityProvider
):

    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[LocalActivityEvent]:

        raise RuntimeError(
            "Planning API unavailable"
        )




@pytest.mark.asyncio
async def test_local_activity_service_collects_events():

    provider = MockPlanningApplicationProvider()

    service = LocalActivityService(
        providers=[provider],
    )

    events = await service.get_events(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.event_type
        == "planning_application_approved"
    )

    assert event.category == "restaurant"

    assert event.status == "approved"

    assert event.source == (
        "planning_authority"
    )

    assert event.source_reference == "PA-001"

@pytest.mark.asyncio
async def test_local_activity_service_reports_successful_provider():

    service = LocalActivityService(
        providers=[
            SuccessfulLocalActivityProvider(),
        ],
    )

    results = await service.get_events_with_status(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(results) == 1

    result = results[0]

    assert result.status == (
        ProviderStatus.SUCCESS
    )

    assert result.provider == (
        "SuccessfulLocalActivityProvider"
    )

    assert len(result.events) == 1

    assert result.events[0].category == (
        "restaurant"
    )

    assert result.error is None

@pytest.mark.asyncio
async def test_local_activity_service_reports_unavailable_provider():

    service = LocalActivityService(
        providers=[
            FailingLocalActivityProvider(),
        ],
    )

    results = await service.get_events_with_status(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(results) == 1

    result = results[0]

    assert result.status == (
        ProviderStatus.UNAVAILABLE
    )

    assert result.provider == (
        "FailingLocalActivityProvider"
    )

    assert result.events == []

    assert result.error == (
        "Planning API unavailable"
    )

@pytest.mark.asyncio
async def test_local_activity_service_preserves_success_when_provider_fails():

    service = LocalActivityService(
        providers=[
            SuccessfulLocalActivityProvider(),
            FailingLocalActivityProvider(),
        ],
    )

    results = await service.get_events_with_status(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(results) == 2

    successful_result = results[0]
    failed_result = results[1]

    assert successful_result.status == (
        ProviderStatus.SUCCESS
    )

    assert len(
        successful_result.events
    ) == 1

    assert failed_result.status == (
        ProviderStatus.UNAVAILABLE
    )

    assert failed_result.events == []

    assert failed_result.error == (
        "Planning API unavailable"
    )

@pytest.mark.asyncio
async def test_local_activity_service_get_events_returns_successful_events():

    service = LocalActivityService(
        providers=[
            SuccessfulLocalActivityProvider(),
        ],
    )

    events = await service.get_events(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(events) == 1

    assert events[0].category == (
        "restaurant"
    )




