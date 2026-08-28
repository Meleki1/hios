import pytest

from hios.capabilities.intelligence.collectors.explicit_intent import (
    ExplicitIntentCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)

@pytest.mark.asyncio
async def test_explicit_intents_become_signals():

    collector = ExplicitIntentCollector()

    signals = await collector.collect(
        subject_id="household-1",
        intents=[
            "reported_active_problem",
            "asked_for_price",
        ],
    )

    assert len(signals) == 2

    assert all(
        signal.type == SignalType.EXPLICIT_INTENT
        for signal in signals
    )

    assert signals[0].value == (
        "reported_active_problem"
    )

    assert signals[1].value == "asked_for_price"

@pytest.mark.asyncio
async def test_explicit_intents_become_signals():

    collector = ExplicitIntentCollector()

    signals = await collector.collect(
        subject_id="subject-123",
        intents=[
            "requested_treatment",
            "asked_for_price",
        ],
    )

    assert len(signals) == 2

    assert all(
        signal.type == SignalType.EXPLICIT_INTENT
        for signal in signals
    )

    assert signals[0].value == (
        "requested_treatment"
    )

    assert signals[1].value == (
        "asked_for_price"
    )

@pytest.mark.asyncio
async def test_explicit_intent_signals_are_scored():

    collector = ExplicitIntentCollector()
    scorer = RuleBasedIntentScorer()

    signals = await collector.collect(
        subject_id="subject-123",
        intents=[
            "requested_treatment",
            "asked_for_price",
        ],
    )

    result = await scorer.score(
        signals,
    )

    assert result.score == 70.0
    assert result.level == IntentLevel.HIGH