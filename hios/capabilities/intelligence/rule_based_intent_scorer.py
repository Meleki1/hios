from hios.capabilities.intelligence.intent_scorer import (
    IntentScorer,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.signal import Signal


class RuleBasedIntentScorer(IntentScorer):

    WEIGHTS = {
        "asked_for_price": 40.0,
        "requested_treatment": 30.0,
        "reported_active_problem": 25.0,
        "return_visits": 10.0,
        "price_comparisons": 10.0,
        "contractor_searches": 15.0,
    }

    async def score(
        self,
        signals: list[Signal],
    ) -> IntentScore:

        total = 0.0

        for signal in signals:

            if signal.value not in self.WEIGHTS:
                    continue

            weight = self.WEIGHTS[
                signal.value
            ]

            total += (
                weight
                * signal.strength
                * signal.confidence
            )

        score = min(total, 100.0)

        if score >= 70:
            level = IntentLevel.HIGH
        elif score >= 40:
            level = IntentLevel.MEDIUM
        else:
            level = IntentLevel.LOW

        return IntentScore(
            score=score,
            level=level,
            confidence=1.0,
            signals=signals,
        )