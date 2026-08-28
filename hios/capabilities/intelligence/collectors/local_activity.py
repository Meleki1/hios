from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import SignalSource
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.local_activity.models.local_activity_trend import LocalActivityTrend

class LocalActivitySignalCollector:

    async def collect(
        self,
        subject_id: str,
        activities: dict[str, str],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.LOCAL_ACTIVITY,
                source=SignalSource.LOCAL_ACTIVITY,
                name=name,
                value=value,
            )
            for name, value in activities.items()
        ]

    async def collect_events(
        self,
        subject_id: str,
        events: list[LocalActivityEvent],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.LOCAL_ACTIVITY,
                source=SignalSource.LOCAL_ACTIVITY,
                name=event.event_type,
                value=event.category,
                strength=1.0,
                confidence=1.0,
                observed_at=event.observed_at,
                metadata={
                    "source": event.source,
                    **event.metadata,
                    **(
                        {
                            "status": event.status,
                        }
                        if event.status is not None
                        else {}
                    ),
                    **(
                        {
                            "latitude": str(
                                event.latitude
                            )
                        }
                        if event.latitude is not None
                        else {}
                    ),
                    **(
                        {
                            "longitude": str(
                                event.longitude
                            )
                        }
                        if event.longitude is not None
                        else {}
                    ),
                    **(
                        {
                            "source_reference": (
                                event.source_reference
                            )
                        }
                        if event.source_reference is not None
                        else {}
                    ),
                },
            )
            for event in events
        ]

    async def collect_trends(
        self,
        subject_id: str,
        trends: list[LocalActivityTrend],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.LOCAL_ACTIVITY,
                source=SignalSource.LOCAL_ACTIVITY,
                name=f"local_activity_{trend.category}",
                value=trend.trend,
                strength=trend.intensity,
                confidence=1.0,
                metadata={
                    "category": trend.category,
                    "event_count": str(
                        trend.event_count
                    ),
                    "intensity": str(
                        trend.intensity
                    ),
                },
            )
            for trend in trends
        ]