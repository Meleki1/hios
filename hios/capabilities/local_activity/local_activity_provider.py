from abc import ABC, abstractmethod

from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.local_activity.models.provider_result import LocalActivityProviderResult


class LocalActivityProvider(ABC):

    @abstractmethod
    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[LocalActivityEvent]:
        raise NotImplementedError