from abc import ABC, abstractmethod
from hios.capabilities.local_activity.models.planning_application import PlanningApplication


class PlanningApplicationProvider(ABC):

    @abstractmethod
    async def get_recent_applications(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[PlanningApplication]:
        raise NotImplementedError