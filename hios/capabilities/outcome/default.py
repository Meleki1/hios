from hios.capabilities.execution.models.status import (
    ExecutionStatus,
)

from hios.capabilities.execution.models.execution import (
    Execution,
)

from hios.capabilities.outcome.evaluator import (
    OutcomeEvaluator,
)

from hios.capabilities.outcome.models.outcome import (
    Outcome,
)

from hios.capabilities.outcome.models.status import (
    OutcomeStatus,
)


class DefaultOutcomeEvaluator(
    OutcomeEvaluator,
):

    def evaluate(
        self,
        execution: Execution,
    ) -> Outcome:

        match execution.status:

            case ExecutionStatus.SUCCESS:
                status = OutcomeStatus.SUCCESS

            case ExecutionStatus.FAILED:
                status = OutcomeStatus.FAILED

            case _:
                status = OutcomeStatus.UNKNOWN

        return Outcome(
            execution=execution,
            status=status,
        )