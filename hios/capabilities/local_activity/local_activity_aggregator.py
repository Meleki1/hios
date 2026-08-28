from collections import Counter
from datetime import datetime, timedelta, timezone

from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)
from hios.capabilities.local_activity.models.local_activity_trend import (
    LocalActivityTrend,
)


class LocalActivityAggregator:

    def aggregate(
        self,
        events: list[LocalActivityEvent],
        window_days: int = 30,
        now: datetime | None = None,
    ) -> list[LocalActivityTrend]:

        if not events:
            return []

        if now is None:
            now = datetime.now(timezone.utc)

        cutoff = now - timedelta(
            days=window_days,
        )

        recent_events = [
            event
            for event in events
            if event.observed_at >= cutoff
        ]

        if not recent_events:
            return []

        counts = Counter(
            event.category
            for event in recent_events
        )

        trends = []

        for category, count in counts.items():

            intensity = min(
                count / 10.0,
                1.0,
            )

            if intensity >= 0.7:
                trend = "high"
            elif intensity >= 0.3:
                trend = "moderate"
            else:
                trend = "low"

            trends.append(
                LocalActivityTrend(
                    category=category,
                    event_count=count,
                    intensity=intensity,
                    trend=trend,
                )
            )

        return trends