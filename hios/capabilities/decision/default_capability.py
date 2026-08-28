from hios.runtime.context import RuntimeContext

from hios.capabilities.decision.capability import DecisionCapability
from hios.capabilities.decision.contract import (
    DecisionRequest,
    DecisionResult,
)
from hios.capabilities.decision.selector import DecisionSelector


class DefaultDecisionCapability(
    DecisionCapability,
):

    def __init__(
        self,
        selector: DecisionSelector,
    ):
        self._selector = selector

    async def reason(
        self,
        request: DecisionRequest,
        context: RuntimeContext,
    ) -> DecisionResult:

        decision = self._selector.select(
            request.plans,
        )

        return DecisionResult(
            decision=decision,
        )