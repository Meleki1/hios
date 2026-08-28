from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class PlatformBehaviourSignalCollector:

    async def collect(
        self,
        subject_id: str,
        behaviours: dict[str, str],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.PLATFORM_BEHAVIOUR,
                source=SignalSource.PLATFORM,
                name=name,
                value=value,
            )
            for name, value in behaviours.items()
        ]