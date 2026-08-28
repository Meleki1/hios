from hios.capabilities.local_activity.local_activity_provider import LocalActivityProvider
from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.local_activity.models.provider_result import LocalActivityProviderResult, ProviderStatus


class LocalActivityService:

    def __init__(
        self,
        providers: list[LocalActivityProvider],
    ):
        self._providers = providers

    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
    ) -> list[LocalActivityEvent]:

        results = await self.get_events_with_status(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
        )

        events: list[LocalActivityEvent] = []

        for result in results:
            events.extend(result.events)

        return events

    
    async def get_events_with_status(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5.0,
    ) -> list[LocalActivityProviderResult]:

        results: list[
            LocalActivityProviderResult
        ] = []

        for provider in self._providers:

            provider_name = (
                provider.__class__.__name__
            )

            try:

                events = await provider.get_events(
                    latitude=latitude,
                    longitude=longitude,
                    radius_km=radius_km,
                )

                results.append(
                    LocalActivityProviderResult(
                        status=ProviderStatus.SUCCESS,
                        provider=provider_name,
                        events=events,
                    )
                )

            except Exception as exc:

                results.append(
                    LocalActivityProviderResult(
                        status=ProviderStatus.UNAVAILABLE,
                        provider=provider_name,
                        error=str(exc),
                    )
                )

        return results