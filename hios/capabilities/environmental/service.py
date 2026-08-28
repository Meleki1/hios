from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.providers.base import (
    EnvironmentalProvider,
)


class EnvironmentalService:

    def __init__(
        self,
        provider: EnvironmentalProvider,
    ):
        self._provider = provider

    async def get_observation(
        self,
        latitude: float,
        longitude: float,
    ) -> EnvironmentalObservation | None:

        return await self._provider.get_observation(
            latitude=latitude,
            longitude=longitude,
        )

    def to_observations(
        self,
        observation: EnvironmentalObservation,
    ) -> dict[str, str]:

        observations: dict[str, str] = {}

        if observation.rainfall_mm is not None:
            observations["rainfall_mm"] = str(
                observation.rainfall_mm
            )

        if observation.temperature_c is not None:
            observations["temperature_c"] = str(
                observation.temperature_c
            )

        if observation.humidity_percent is not None:
            observations["humidity_percent"] = str(
                observation.humidity_percent
            )

        if observation.wind_speed_mps is not None:
            observations["wind_speed_mps"] = str(
                observation.wind_speed_mps
            )

        if observation.frost is not None:
            observations["frost"] = str(
                observation.frost
            )

        return observations