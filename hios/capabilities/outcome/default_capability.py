from hios.runtime.context import RuntimeContext

from hios.capabilities.outcome.contract import (
    OutcomeCapability,
)
from hios.capabilities.outcome.contract import (
    OutcomeRequest,
    OutcomeResult,
)
from hios.capabilities.outcome.evaluator import (
    OutcomeEvaluator,
)


class DefaultOutcomeCapability(
    OutcomeCapability,
):

    def __init__(
        self,
        evaluator: OutcomeEvaluator,
    ):

        self._evaluator = evaluator

    async def reason(
        self,
        request: OutcomeRequest,
        context: RuntimeContext,
    ) -> OutcomeResult:

        outcome = self._evaluator.evaluate(
            request.execution.execution,
        )

        return OutcomeResult(
            outcome=outcome,
        )