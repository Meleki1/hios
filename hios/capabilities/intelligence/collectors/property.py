from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class PropertySignalCollector:

    async def collect(
        self,
        subject_id: str,
        characteristics: dict[str, str],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.PROPERTY,
                source=SignalSource.PROPERTY,
                name=name,
                value=value,
            )
            for name, value in characteristics.items()
        ]