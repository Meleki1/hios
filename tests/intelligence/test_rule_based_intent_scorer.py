import pytest

from hios.capabilities.intelligence.models.intent_score import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
)


@pytest.mark.asyncio
async def test_high_intent_is_detected():

    scorer = RuleBasedIntentScorer()

    signals = [
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="asked_for_price",
        ),
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="reported_active_problem",
        ),
    ]

    result = await scorer.score(signals)

    assert result.score == 65.0
    assert result.level == IntentLevel.MEDIUM
    assert len(result.signals) == 2


@pytest.mark.asyncio
async def test_signal_strength_and_confidence_affect_score():

    scorer = RuleBasedIntentScorer()

    signals = [
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="asked_for_price",
            strength=0.5,
            confidence=0.8,
        ),
    ]

    result = await scorer.score(signals)

    assert result.score == 16.0


@pytest.mark.asyncio
async def test_empty_signals_produce_low_intent():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score([])

    assert result.score == 0.0
    assert result.level == IntentLevel.LOW

@pytest.mark.asyncio
async def test_score_is_capped_at_100():

    scorer = RuleBasedIntentScorer()

    signals = [
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="asked_for_price",
        ),
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="requested_treatment",
        ),
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="reported_active_problem",
        ),
    ]

    result = await scorer.score(signals)

    assert result.score == 95.0


@pytest.mark.asyncio
async def test_contextual_signals_do_not_increase_intent_score():

    scorer = RuleBasedIntentScorer()

    signals = [
        Signal(
            type=SignalType.PROPERTY,
            source=SignalSource.PROPERTY,
            name="year_built",
            value="1890",
        ),
        Signal(
            type=SignalType.ENVIRONMENTAL,
            source=SignalSource.WEATHER,
            name="rainfall_mm",
            value="42.0",
        ),
    ]

    result = await scorer.score(signals)

    assert result.score == 0.0
    assert result.level == IntentLevel.LOW
    assert result.signals == signals

@pytest.mark.asyncio
async def test_rule_based_intent_scorer_scores_known_signals():

    scorer = RuleBasedIntentScorer()

    signals = [
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="reported_active_problem",
            strength=1.0,
            confidence=1.0,
        ),
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="requested_treatment",
            strength=1.0,
            confidence=1.0,
        ),
        Signal(
            type=SignalType.EXPLICIT_INTENT,
            source=SignalSource.HOME_ASSIST,
            name="intent",
            value="asked_for_price",
            strength=1.0,
            confidence=1.0,
        ),
    ]

    result = await scorer.score(signals)

    assert result.score == 95.0
    assert result.level == IntentLevel.HIGH