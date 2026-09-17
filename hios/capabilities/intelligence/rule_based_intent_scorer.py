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
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class RuleBasedIntentScorer(IntentScorer):
    """
    "Start with statistics" scorer (per the product docs), not ML --
    a fixed point table per signal, summed and capped at 100.

    Originally this only understood EXPLICIT_INTENT signals (a
    small fixed vocabulary -- "asked_for_price" etc. -- where
    signal.value IS the category, so a flat {value: weight} lookup
    works). PROPERTY/ENVIRONMENTAL/LOCAL_ACTIVITY/CONVERSATION/
    PLATFORM_BEHAVIOUR signals were (or, for the latter two, are
    now) collected elsewhere in the pipeline but never moved the
    score at all: their .value is raw data (a postcode, "42.0" mm
    of rain, a trend label, a visit count), not a small fixed
    vocabulary, so a flat {value: weight} table can't score them --
    "52.3" and "52.4" of rainfall aren't meaningfully different
    weight-table entries, and a bare {value: weight} lookup would
    also silently conflate unrelated signal categories that happen
    to share a value (every LOCAL_ACTIVITY trend reports value
    "high"/"moderate"/"low" regardless of what it's a trend *of*).

    So those categories are scored with small, explicit
    signal.name-keyed threshold rules instead of a flat table --
    see _score_property/_score_environmental/_score_local_activity/
    _score_conversation/_score_platform_behaviour below. Each rule
    is grounded in a specific worked example from the product docs
    where one exists (cited inline); this is a deliberately small
    starting set covering only the fields the platform actually
    collects today (see PropertyService.to_characteristics /
    EnvironmentalService.to_observations / the `intelligence` node
    in assistant/graph/nodes.py for where interactions/
    platform_behaviours are derived) -- not every signal the docs
    mention has a real data source wired up yet (e.g. garden size,
    nearby woodland, flood risk aren't fields on PropertyProfile;
    "saved_advice"/"price_comparisons" as platform behaviour have no
    producer yet either), so there was nothing honest to score for
    those. Easy to extend as more fields/providers land, and all the
    point values here are starting points to retune once real
    outcome data exists (see the intelligence-pipeline-wiring-audit
    project doc's prediction feedback loop section).
    """

    WEIGHTS = {
        "asked_for_price": 40.0,
        "requested_treatment": 30.0,
        "reported_active_problem": 25.0,
        "return_visits": 10.0,
        "price_comparisons": 10.0,
        "contractor_searches": 15.0,
    }

    PROPERTY_PRE_1950_YEAR_BUILT = 8.0
    PROPERTY_HAS_BASEMENT = 5.0
    ENVIRONMENTAL_RAINFALL_HEAVY_MM = 50.0
    ENVIRONMENTAL_RAINFALL_HEAVY_POINTS = 10.0
    ENVIRONMENTAL_RAINFALL_MODERATE_MM = 25.0
    ENVIRONMENTAL_RAINFALL_MODERATE_POINTS = 5.0
    LOCAL_ACTIVITY_TREND_POINTS = {
        "high": 15.0,
        "moderate": 8.0,
        "low": 0.0,
    }
    CONVERSATION_PROGRESSION_POINTS = 20.0

    PLATFORM_RETURN_VISITS_HIGH_THRESHOLD = 4
    PLATFORM_RETURN_VISITS_HIGH_POINTS = 15.0
    PLATFORM_RETURN_VISITS_MODERATE_THRESHOLD = 2
    PLATFORM_RETURN_VISITS_MODERATE_POINTS = 5.0

    async def score(
        self,
        signals: list[Signal],
    ) -> IntentScore:

        total = 0.0

        for signal in signals:

            weight = self._weight_for(signal)

            if weight is None:
                continue

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

    def _weight_for(
        self,
        signal: Signal,
    ) -> float | None:

        if signal.type == SignalType.PROPERTY:
            return self._score_property(signal)

        if signal.type == SignalType.ENVIRONMENTAL:
            return self._score_environmental(signal)

        if signal.type == SignalType.LOCAL_ACTIVITY:
            return self._score_local_activity(signal)

        if signal.type == SignalType.CONVERSATION:
            return self._score_conversation(signal)

        if signal.type == SignalType.PLATFORM_BEHAVIOUR:
            return self._score_platform_behaviour(signal)

        return self.WEIGHTS.get(signal.value)

    def _score_property(
        self,
        signal: Signal,
    ) -> float | None:

        if signal.name == "year_built":
            try:
                year_built = int(signal.value)
            except (TypeError, ValueError):
                return None

            if year_built < 1950:
                return self.PROPERTY_PRE_1950_YEAR_BUILT

            return None

        if signal.name == "has_basement":
            if signal.value == "True":
                return self.PROPERTY_HAS_BASEMENT

            return None

        return None

    def _score_environmental(
        self,
        signal: Signal,
    ) -> float | None:

        if signal.name != "rainfall_mm":
            return None

        try:
            rainfall = float(signal.value)
        except (TypeError, ValueError):
            return None

        if rainfall >= self.ENVIRONMENTAL_RAINFALL_HEAVY_MM:
            return self.ENVIRONMENTAL_RAINFALL_HEAVY_POINTS

        if rainfall >= self.ENVIRONMENTAL_RAINFALL_MODERATE_MM:
            return self.ENVIRONMENTAL_RAINFALL_MODERATE_POINTS

        return None

    def _score_local_activity(
        self,
        signal: Signal,
    ) -> float | None:

        if not signal.name.startswith("local_activity_"):
            return None

        return self.LOCAL_ACTIVITY_TREND_POINTS.get(
            signal.value,
        )

    def _score_conversation(
        self,
        signal: Signal,
    ) -> float | None:

        if signal.name == "conversation_progression":
            return self.CONVERSATION_PROGRESSION_POINTS

        return None

    def _score_platform_behaviour(
        self,
        signal: Signal,
    ) -> float | None:

        if signal.name != "return_visits":
            return None

        try:
            return_visits = int(signal.value)
        except (TypeError, ValueError):
            return None

        if (
            return_visits
            >= self.PLATFORM_RETURN_VISITS_HIGH_THRESHOLD
        ):
            return self.PLATFORM_RETURN_VISITS_HIGH_POINTS

        if (
            return_visits
            >= self.PLATFORM_RETURN_VISITS_MODERATE_THRESHOLD
        ):
            return self.PLATFORM_RETURN_VISITS_MODERATE_POINTS

        return None