from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.providers.base import (
    EnvironmentalProvider,
)


class MockEnvironmentalProvider(
    EnvironmentalProvider
):

    async def get_observation(
        self,
        latitude: float,
        longitude: float,
    ) -> EnvironmentalObservation | None:

        return EnvironmentalObservation(
            rainfall_mm=42.0,
            temperature_c=18.5,
            humidity_percent=78.0,
            wind_speed_mps=4.2,
            frost=False,
        )