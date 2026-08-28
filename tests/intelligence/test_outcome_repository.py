import pytest

from hios.capabilities.intelligence.models.outcome import Outcome


class FakeOutcomeRepository:

    def __init__(self):
        self.outcomes: dict[str, Outcome] = {}

    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:

        self.outcomes[outcome.id] = outcome

        return outcome

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:

        for outcome in self.outcomes.values():

            if outcome.prediction_id == prediction_id:
                return outcome

        return None


@pytest.mark.asyncio
async def test_outcome_repository_saves_and_retrieves():

    repository = FakeOutcomeRepository()

    outcome = Outcome(
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    saved = await repository.save(outcome)

    assert saved.id == outcome.id

    retrieved = await repository.get_by_prediction(
        "prediction-1",
    )

    assert retrieved is not None
    assert retrieved.id == outcome.id
    assert retrieved.occurred is True