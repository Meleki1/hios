from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import SignalSource
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation


class EnvironmentalSignalCollector:

    async def collect(
        self,
        observation: EnvironmentalObservation,
    ) -> list[Signal]:

        signals: list[Signal] = []

        if observation.rainfall_mm is not None:
            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name="rainfall",
                    value=str(
                        observation.rainfall_mm
                    ),
                )
            )

        if observation.temperature_c is not None:
            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name="temperature",
                    value=str(
                        observation.temperature_c
                    ),
                )
            )

        if observation.humidity_percent is not None:
            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name="humidity",
                    value=str(
                        observation.humidity_percent
                    ),
                )
            )

        if observation.wind_speed_mps is not None:
            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name="wind_speed",
                    value=str(
                        observation.wind_speed_mps
                    ),
                )
            )

        if observation.frost is not None:
            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name="frost",
                    value=str(
                        observation.frost
                    ),
                )
            )

        return signals