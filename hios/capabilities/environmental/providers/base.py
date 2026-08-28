from abc import ABC, abstractmethod

from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)


class EnvironmentalProvider(ABC):

    @abstractmethod
    async def get_observation(
        self,
        latitude: float,
        longitude: float,
    ) -> EnvironmentalObservation | None:
        raise NotImplementedError