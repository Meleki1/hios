import pytest

from hios.capabilities.intelligence.models.intent_score import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.signal import (
    Signal,
    SignalSource,
    SignalType,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
)


def make_signal(
    value: str,
    strength: float = 1.0,
    confidence: float = 1.0,
) -> Signal:

    return Signal(
        type=SignalType.EXPLICIT_INTENT,
        source=SignalSource.HOME_ASSIST,
        name=value,
        value=value,
        strength=strength,
        confidence=confidence,
    )


@pytest.mark.asyncio
async def test_rule_based_scorer_scores_known_signal():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "reported_active_problem",
            )
        ]
    )

    assert result.score == 25.0
    assert result.level == IntentLevel.LOW
    assert result.confidence == 1.0


@pytest.mark.asyncio
async def test_rule_based_scorer_applies_signal_strength():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "reported_active_problem",
                strength=0.5,
            )
        ]
    )

    assert result.score == 12.5


@pytest.mark.asyncio
async def test_rule_based_scorer_applies_signal_confidence():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "reported_active_problem",
                confidence=0.5,
            )
        ]
    )

    assert result.score == 12.5


@pytest.mark.asyncio
async def test_rule_based_scorer_combines_multiple_signals():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "reported_active_problem",
            ),
            make_signal(
                "requested_treatment",
            ),
            make_signal(
                "asked_for_price",
            ),
        ]
    )

    assert result.score == 95.0
    assert result.level == IntentLevel.HIGH


@pytest.mark.asyncio
async def test_rule_based_scorer_caps_score_at_100():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "asked_for_price",
            ),
            make_signal(
                "requested_treatment",
            ),
            make_signal(
                "reported_active_problem",
            ),
            make_signal(
                "return_visits",
            ),
            make_signal(
                "contractor_searches",
            ),
        ]
    )

    assert result.score == 100.0
    assert result.level == IntentLevel.HIGH


@pytest.mark.asyncio
async def test_rule_based_scorer_ignores_unknown_signal():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "unknown_signal",
            )
        ]
    )

    assert result.score == 0.0
    assert result.level == IntentLevel.LOW


@pytest.mark.asyncio
async def test_rule_based_scorer_medium_intent():

    scorer = RuleBasedIntentScorer()

    result = await scorer.score(
        [
            make_signal(
                "requested_treatment",
            ),
            make_signal(
                "return_visits",
            ),
        ]
    )

    assert result.score == 40.0
    assert result.level == IntentLevel.MEDIUM


@pytest.mark.asyncio
async def test_rule_based_scorer_preserves_signals():

    scorer = RuleBasedIntentScorer()

    signals = [
        make_signal(
            "reported_active_problem",
        ),
    ]

    result = await scorer.score(
        signals,
    )

    assert result.signals == signals
    assert len(result.signals) == 1