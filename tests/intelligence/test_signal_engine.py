import pytest

from hios.capabilities.intelligence.basic_signal_engine import (
    BasicSignalEngine,
)
from hios.capabilities.intelligence.collectors.conversation import (
    ConversationSignalCollector,
)
from hios.capabilities.intelligence.collectors.environmental import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.collectors.explicit_intent import (
    ExplicitIntentCollector,
)
from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)
from hios.capabilities.intelligence.collectors.platform import (
    PlatformBehaviourSignalCollector,
)
from hios.capabilities.intelligence.collectors.property import (
    PropertySignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_signal_engine_collects_all_signal_categories():

    engine = BasicSignalEngine(
        explicit_intent_collector=ExplicitIntentCollector(),
        conversation_collector=ConversationSignalCollector(),
        property_collector=PropertySignalCollector(),
        environmental_collector=EnvironmentalSignalCollector(),
        local_activity_collector=LocalActivitySignalCollector(),
        platform_behaviour_collector=(
            PlatformBehaviourSignalCollector()
        ),
    )

    signals = await engine.collect(
        subject_id="household-1",
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "asked_about_pests",
        ],
        property_characteristics={
            "has_loft": "true",
        },
        environmental_observations={
            "rainfall": "42mm",
        },
        local_activities={
            "local_pest_reports": "increasing",
        },
        platform_behaviours={
            "return_visits": "3",
        },
    )

    assert len(signals) == 6

    signal_types = {
        signal.type
        for signal in signals
    }

    assert signal_types == {
        SignalType.EXPLICIT_INTENT,
        SignalType.CONVERSATION,
        SignalType.PROPERTY,
        SignalType.ENVIRONMENTAL,
        SignalType.LOCAL_ACTIVITY,
        SignalType.PLATFORM_BEHAVIOUR,
    }