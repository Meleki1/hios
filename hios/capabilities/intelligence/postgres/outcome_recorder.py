from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.postgres.repository import (
    PostgresOutcomeRepository,
)


class PostgresOutcomeRecorder:

    def __init__(
        self,
        repository: PostgresOutcomeRepository,
    ):
        self._repository = repository

    async def record(
        self,
        outcome: Outcome,
    ) -> Outcome:

        return await self._repository.save(
            outcome,
        )