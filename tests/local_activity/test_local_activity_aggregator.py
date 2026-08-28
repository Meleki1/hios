from hios.capabilities.local_activity.local_activity_aggregator import (
    LocalActivityAggregator,
)
from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)
from datetime import datetime, timedelta, timezone


def test_local_activity_aggregator_groups_events_by_category():

    events = [
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
        ),
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
        ),
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
        ),
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="hotel",
            source="planning_authority",
        ),
    ]

    aggregator = LocalActivityAggregator()

    trends = aggregator.aggregate(
        events,
    )

    assert len(trends) == 2

    restaurant = next(
        trend
        for trend in trends
        if trend.category == "restaurant"
    )

    assert restaurant.event_count == 3
    assert restaurant.intensity == 0.3
    assert restaurant.trend == "moderate"

    hotel = next(
        trend
        for trend in trends
        if trend.category == "hotel"
    )

    assert hotel.event_count == 1
    assert hotel.intensity == 0.1
    assert hotel.trend == "low"


def test_local_activity_aggregator_handles_empty_events():

    aggregator = LocalActivityAggregator()

    trends = aggregator.aggregate([])

    assert trends == []

def test_local_activity_aggregator_uses_time_window():

    now = datetime(
        2026,
        8,
        10,
        tzinfo=timezone.utc,
    )

    events = [
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
            observed_at=(
                now - timedelta(days=5)
            ),
        ),
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
            observed_at=(
                now - timedelta(days=10)
            ),
        ),
        LocalActivityEvent(
            event_type="planning_application_approved",
            category="restaurant",
            source="planning_authority",
            observed_at=(
                now - timedelta(days=90)
            ),
        ),
    ]

    aggregator = LocalActivityAggregator()

    trends = aggregator.aggregate(
        events,
        window_days=30,
        now=now,
    )

    assert len(trends) == 1

    restaurant = trends[0]

    assert restaurant.category == "restaurant"
    assert restaurant.event_count == 2