import pytest

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.postgres.repository import (
    PostgresOutcomeRepository,
)
from sqlalchemy import select

from hios.capabilities.intelligence.postgres.models.outcome import (
    OutcomeRecord,
)
from hios.db.session import SessionLocal


@pytest.mark.asyncio
@pytest.mark.integration
async def test_outcome_repository_persists_and_retrieves():

    outcome = Outcome(
        prediction_id="prediction-integration-1",
        subject_id="household-integration-1",
        target="pest_control_need",
        occurred=True,
        details={
            "service_requested": "true",
        },
    )

    async with SessionLocal() as session:

        repository = PostgresOutcomeRepository(
            session=session,
        )

        saved = await repository.save(
            outcome,
        )

        assert saved.id == outcome.id

        retrieved = (
            await repository.get_by_prediction(
                "prediction-integration-1",
            )
        )

        assert retrieved is not None
        assert retrieved.id == outcome.id
        assert retrieved.prediction_id == (
            "prediction-integration-1"
        )
        assert retrieved.subject_id == (
            "household-integration-1"
        )
        assert retrieved.target == (
            "pest_control_need"
        )
        assert retrieved.occurred is True

       






"""retrieved = (
            await repository.get_by_prediction(
                "prediction-integration-1",
            )
        )

        assert retrieved is not None

        assert retrieved.id == outcome.id
        assert (
            retrieved.prediction_id
            == "prediction-integration-1"
        )
        assert (
            retrieved.subject_id
            == "household-integration-1"
        )
        assert (
            retrieved.target
            == "pest_control_need"
        )
        assert retrieved.occurred is True
        assert retrieved.details == {
            "service_requested": "true",
        }"""