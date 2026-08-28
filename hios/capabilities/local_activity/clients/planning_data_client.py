from abc import ABC, abstractmethod


class PlanningDataClient(ABC):

    @abstractmethod
    async def search(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[dict]:
        raise NotImplementedError