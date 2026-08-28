import pytest

from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


@pytest.mark.asyncio
async def test_local_activity_becomes_signals():

    collector = LocalActivitySignalCollector()

    signals = await collector.collect(
        subject_id="household-1",
        activities={
            "construction_activity": "high",
            "local_pest_reports": "increasing",
            "waste_change": "new_collection_schedule",
        },
    )

    assert len(signals) == 3

    assert all(
        signal.type == SignalType.LOCAL_ACTIVITY
        for signal in signals
    )

    assert signals[0].name == "construction_activity"
    assert signals[0].value == "high"

    assert signals[1].name == "local_pest_reports"
    assert signals[1].value == "increasing"