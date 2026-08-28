import pytest

from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.service import (
    IntelligenceService,
)


class FakeSignalEngine:

    async def collect(
        self,
        subject_id: str,
        **kwargs,
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.EXPLICIT_INTENT,
                source=SignalSource.HOME_ASSIST,
                name="intent",
                value="asked_for_price",
            )
        ]


class FakeIntentScorer:

    async def score(
        self,
        signals: list[Signal],
    ) -> IntentScore:

        return IntentScore(
            score=40.0,
            level=IntentLevel.MEDIUM,
            confidence=1.0,
            signals=signals,
        )


@pytest.mark.asyncio
async def test_intelligence_service_orchestrates_analysis():

    service = IntelligenceService(
        signal_engine=FakeSignalEngine(),
        intent_scorer=FakeIntentScorer(),
    )

    result = await service.analyze(
        subject_id="household-1",
    )

    assert result.score == 40.0
    assert result.level == IntentLevel.MEDIUM
    assert len(result.signals) == 1