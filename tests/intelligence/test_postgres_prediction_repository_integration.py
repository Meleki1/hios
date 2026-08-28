import pytest

from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.postgres.prediction_repository import (
    PostgresPredictionRepository,
)
from hios.db.session import SessionLocal


@pytest.mark.asyncio
@pytest.mark.integration
async def test_prediction_repository_persists_and_retrieves():

    prediction = Prediction(
        subject_id="household-prediction-integration-1",
        target="pest_control_need",
        horizon_days=90,
        probability=None,
        confidence=1.0,
        evidence=[
            "asked_for_price",
            "reported_active_problem",
        ],
        intent_score=IntentScore(
            score=65.0,
            level=IntentLevel.MEDIUM,
            confidence=1.0,
            signals=[],
        ),
    )

    async with SessionLocal() as session:

        repository = PostgresPredictionRepository(
            session=session,
        )

        saved = await repository.save(
            prediction,
        )

        assert saved.id == prediction.id

        retrieved = await repository.get_by_id(
            prediction.id,
        )

        assert retrieved is not None

        assert retrieved.id == prediction.id
        assert (
            retrieved.subject_id
            == "household-prediction-integration-1"
        )
        assert retrieved.target == "pest_control_need"
        assert retrieved.horizon_days == 90
        assert retrieved.probability is None
        assert retrieved.confidence == 1.0

        assert retrieved.evidence == [
            "asked_for_price",
            "reported_active_problem",
        ]

        assert retrieved.intent_score.score == 65.0
        assert (
            retrieved.intent_score.level
            == IntentLevel.MEDIUM
        )