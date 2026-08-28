import pytest

from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.postgres.prediction_evaluation_repository import (
    PostgresPredictionEvaluationRepository,
)
from hios.db.session import SessionLocal


@pytest.mark.asyncio
@pytest.mark.integration
async def test_prediction_evaluation_repository_persists_and_retrieves():

    evaluation = PredictionEvaluation(
        prediction_id="prediction-evaluation-integration-1",
        outcome_id="outcome-evaluation-integration-1",
        correct=True,
        details={
            "reason": "predicted_event_occurred",
        },
    )

    async with SessionLocal() as session:

        repository = (
            PostgresPredictionEvaluationRepository(
                session=session,
            )
        )

        saved = await repository.save(
            evaluation,
        )

        assert saved.id == evaluation.id

        retrieved = (
            await repository.get_by_prediction(
                evaluation.prediction_id,
            )
        )

        assert retrieved is not None

        assert retrieved.id == evaluation.id

        assert (
            retrieved.prediction_id
            == evaluation.prediction_id
        )

        assert (
            retrieved.outcome_id
            == evaluation.outcome_id
        )

        assert retrieved.correct is True

        assert retrieved.details == {
            "reason": "predicted_event_occurred",
        }