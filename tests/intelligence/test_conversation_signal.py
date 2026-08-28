import pytest

from hios.capabilities.intelligence.collectors.conversation import (
    ConversationSignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_conversation_interactions_become_signals():

    collector = ConversationSignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        interactions=[
            "asked_about_pests",
            "asked_how_to_remove_them",
            "asked_about_treatment_price",
        ],
    )

    interaction_signals = [
        signal
        for signal in signals
        if signal.name == "interaction"
    ]

    assert len(interaction_signals) == 3

    assert interaction_signals[0].value == (
        "asked_about_pests"
    )

    assert interaction_signals[2].value == (
        "asked_about_treatment_price"
    )

    assert any(
        signal.name == "conversation_progression"
        for signal in signals
    )

@pytest.mark.asyncio
async def test_conversation_progression_is_detected():

    collector = ConversationSignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        interactions=[
            "asked_about_pests",
            "asked_how_to_remove_them",
            "asked_about_treatment_price",
        ],
    )

    assert len(signals) >= 3

    assert any(
        signal.name == "conversation_progression"
        for signal in signals
    )

