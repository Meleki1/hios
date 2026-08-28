import pytest

from hios.capabilities.intelligence.intelligence_pipeline import (
    IntelligencePipeline,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)


class FakeSignalCollectionService:

    def __init__(self):
        self.received = None

    async def collect_and_score(
        self,
        **kwargs,
    ) -> IntentScore:

        self.received = kwargs

        return IntentScore(
            score=75.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=[],
        )


class FakeIntelligenceService:

    def __init__(self):
        self.received = None

    async def predict(
        self,
        **kwargs,
    ) -> Prediction:

        self.received = kwargs

        return Prediction(
            id="prediction-1",
            subject_id=kwargs["subject_id"],
            target=kwargs["target"],
            horizon_days=kwargs["horizon_days"],
            intent_score=kwargs["intent_score"]
        )


@pytest.mark.asyncio
async def test_intelligence_pipeline_collects_scores_and_predicts():

    signal_service = FakeSignalCollectionService()
    intelligence_service = FakeIntelligenceService()

    pipeline = IntelligencePipeline(
        signal_collection_service=signal_service,
        intelligence_service=intelligence_service,
    )

    prediction = await pipeline.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "asked_about_pests",
        ],
    )

    assert prediction.id == "prediction-1"

    assert (
        signal_service.received["subject_id"]
        == "household-1"
    )

    assert (
        intelligence_service.received["subject_id"]
        == "household-1"
    )

    assert (
        intelligence_service.received["target"]
        == "pest_control_need"
    )

    assert (
        intelligence_service.received["horizon_days"]
        == 14
    )

    assert (
        intelligence_service.received["intent_score"].score
        == 75.0
    )

    assert (
        intelligence_service.received["intent_score"].level
        == IntentLevel.HIGH
    )