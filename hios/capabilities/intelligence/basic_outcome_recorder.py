from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.outcome_recorder import (
    OutcomeRecorder,
)


class BasicOutcomeRecorder(OutcomeRecorder):

    async def record(
        self,
        outcome: Outcome,
    ) -> Outcome:

        return outcome