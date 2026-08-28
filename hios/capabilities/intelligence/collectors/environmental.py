from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class EnvironmentalSignalCollector:

    async def collect(
        self,
        subject_id: str,
        observations: dict[str, str],
    ) -> list[Signal]:

        signals: list[Signal] = []

        for name, value in observations.items():

            signals.append(
                Signal(
                    type=SignalType.ENVIRONMENTAL,
                    source=SignalSource.WEATHER,
                    name=name,
                    value=value,
                )
            )

        return signals