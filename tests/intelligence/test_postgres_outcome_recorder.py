import pytest

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.postgres.outcome_recorder import (
    PostgresOutcomeRecorder,
)


class FakeOutcomeRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:

        self.saved = outcome

        return outcome


@pytest.mark.asyncio
async def test_recorder_delegates_to_repository():

    repository = FakeOutcomeRepository()

    recorder = PostgresOutcomeRecorder(
        repository=repository,
    )

    outcome = Outcome(
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    result = await recorder.record(
        outcome,
    )

    assert result.id == outcome.id
    assert repository.saved is outcome