from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class ExplicitIntentCollector:

    async def collect(
        self,
        subject_id: str,
        intents: list[str],
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.EXPLICIT_INTENT,
                source=SignalSource.HOME_ASSIST,
                name="explicit_intent",
                value=intent,
            )
            for intent in intents
        ]