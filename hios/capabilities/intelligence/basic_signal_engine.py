from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.signal_engine import SignalEngine


class BasicSignalEngine(SignalEngine):

    def __init__(
        self,
        explicit_intent_collector,
        conversation_collector,
        property_collector,
        environmental_collector,
        local_activity_collector,
        platform_behaviour_collector,
    ):
        self._explicit_intent_collector = explicit_intent_collector
        self._conversation_collector = conversation_collector
        self._property_collector = property_collector
        self._environmental_collector = environmental_collector
        self._local_activity_collector = local_activity_collector
        self._platform_behaviour_collector = (
            platform_behaviour_collector
        )

    async def collect(
        self,
        subject_id: str,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
    ) -> list[Signal]:

        signals: list[Signal] = []

        if explicit_intents:
            signals.extend(
                await self._explicit_intent_collector.collect(
                    subject_id=subject_id,
                    intents=explicit_intents,
                )
            )

        if interactions:
            signals.extend(
                await self._conversation_collector.collect(
                    subject_id=subject_id,
                    interactions=interactions,
                )
            )

        if property_characteristics:
            signals.extend(
                await self._property_collector.collect(
                    subject_id=subject_id,
                    characteristics=property_characteristics,
                )
            )

        if environmental_observations:
            signals.extend(
                await self._environmental_collector.collect(
                    subject_id=subject_id,
                    observations=environmental_observations,
                )
            )

        if local_activities:
            signals.extend(
                await self._local_activity_collector.collect(
                    subject_id=subject_id,
                    activities=local_activities,
                )
            )

        if platform_behaviours:
            signals.extend(
                await self._platform_behaviour_collector.collect(
                    subject_id=subject_id,
                    behaviours=platform_behaviours,
                )
            )

        return signals