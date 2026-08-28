from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class ConversationSignalCollector:

    async def collect(
        self,
        subject_id: str,
        interactions: list[str],
    ) -> list[Signal]:

        signals = [
            Signal(
                type=SignalType.CONVERSATION,
                source=SignalSource.HOME_ASSIST,
                name="interaction",
                value=interaction,
            )
            for interaction in interactions
        ]

        progression = (
            "asked_about_pests" in interactions
            and "asked_how_to_remove_them" in interactions
            and "asked_about_treatment_price" in interactions
        )

        if progression:
            signals.append(
                Signal(
                    type=SignalType.CONVERSATION,
                    source=SignalSource.HOME_ASSIST,
                    name="conversation_progression",
                    value="progressing_toward_treatment",
                )
            )

        return signals