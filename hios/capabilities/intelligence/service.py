from hios.capabilities.intelligence.intent_scorer import (
    IntentScorer,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.signal_engine import (
    SignalEngine,
)


class IntelligenceService:

    def __init__(
        self,
        signal_engine: SignalEngine,
        intent_scorer: IntentScorer,
    ):
        self._signal_engine = signal_engine
        self._intent_scorer = intent_scorer

    async def analyze(
        self,
        subject_id: str,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
    ) -> IntentScore:

        signals = await self._signal_engine.collect(
            subject_id=subject_id,
            explicit_intents=explicit_intents,
            interactions=interactions,
            property_characteristics=property_characteristics,
            environmental_observations=environmental_observations,
            local_activities=local_activities,
            platform_behaviours=platform_behaviours,
        )

        return await self._intent_scorer.score(
            signals,
        )