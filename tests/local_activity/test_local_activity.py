import pytest
from hios.capabilities.local_activity.local_activity_service import LocalActivityService
from hios.capabilities.local_activity.providers.planning_applications import MockPlanningApplicationProvider
from hios.capabilities.intelligence.collectors.local_activity import LocalActivitySignalCollector
from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.intelligence.models.signal_source import SignalSource
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.local_activity.models.local_activity_trend import LocalActivityTrend


@pytest.mark.asyncio
async def test_local_activity_collector_converts_events_to_signals():

    event = LocalActivityEvent(
        event_type=(
            "planning_application_approved"
        ),
        category="restaurant",
        latitude=51.5074,
        longitude=-0.1278,
        status="approved",
        source="planning_authority",
        source_reference="PA-001",
        metadata={
            "development_type": "restaurant",
        },
    )

    collector = LocalActivitySignalCollector()

    signals = await collector.collect_events(
        subject_id="household-1",
        events=[event],
    )

    assert len(signals) == 1

    signal = signals[0]

    assert signal.type == (
        SignalType.LOCAL_ACTIVITY
    )

    assert signal.source == (
        SignalSource.LOCAL_ACTIVITY
    )

    assert signal.name == (
        "planning_application_approved"
    )

    assert signal.value == "restaurant"

    assert signal.metadata["status"] == (
        "approved"
    )

    assert signal.metadata["development_type"] == (
        "restaurant"
    )

    assert signal.metadata["source"] == (
        "planning_authority"
    )




@pytest.mark.asyncio
async def test_local_activity_collector_converts_trends_to_signals():

    trends = [
        LocalActivityTrend(
            category="restaurant",
            event_count=7,
            intensity=0.7,
            trend="high",
        ),
        LocalActivityTrend(
            category="construction",
            event_count=2,
            intensity=0.2,
            trend="low",
        ),
    ]

    collector = LocalActivitySignalCollector()

    signals = await collector.collect_trends(
        subject_id="household-1",
        trends=trends,
    )

    assert len(signals) == 2

    restaurant = next(
        signal
        for signal in signals
        if signal.name
        == "local_activity_restaurant"
    )

    assert restaurant.type == (
        SignalType.LOCAL_ACTIVITY
    )

    assert restaurant.source == (
        SignalSource.LOCAL_ACTIVITY
    )

    assert restaurant.value == "high"
    assert restaurant.strength == 0.7

    assert restaurant.metadata[
        "category"
    ] == "restaurant"

    assert restaurant.metadata[
        "event_count"
    ] == "7"

    assert restaurant.metadata[
        "intensity"
    ] == "0.7"

@pytest.mark.asyncio
async def test_local_activity_service_passes_geospatial_query_to_provider():

    class FakeLocalActivityProvider:

        def __init__(self):
            self.received = None

        async def get_events(
            self,
            latitude: float,
            longitude: float,
            radius_km: float,
        ):
            self.received = {
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km,
            }

            return []

    provider = FakeLocalActivityProvider()

    service = LocalActivityService(
        providers=[provider],
    )

    events = await service.get_events(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert events == []

    assert provider.received == {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "radius_km": 5.0,
    }

@pytest.mark.asyncio
async def test_local_activity_service_combines_provider_events():

    class FakeProvider:

        def __init__(self, events):
            self.events = events

        async def get_events(
            self,
            latitude: float,
            longitude: float,
            radius_km: float,
        ):
            return self.events

    event_one = LocalActivityEvent(
        event_type="planning_application_approved",
        category="restaurant",
        source="planning_authority",
    )

    event_two = LocalActivityEvent(
        event_type="new_business",
        category="hotel",
        source="business_registry",
    )

    service = LocalActivityService(
        providers=[
            FakeProvider([event_one]),
            FakeProvider([event_two]),
        ],
    )

    events = await service.get_events(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(events) == 2

    assert event_one in events
    assert event_two in events