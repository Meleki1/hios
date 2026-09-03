from __future__ import annotations

from hios.capabilities.understanding.contract import (
    UnderstandingCapability,
    UnderstandingRequest,
    UnderstandingResult,
)

from hios.capabilities.understanding.strategy import (
    UnderstandingStrategy,
)


class RuleUnderstandingCapability(
    UnderstandingCapability,
):

    def __init__(
        self,
        strategy: UnderstandingStrategy,
    ):
        self._strategy = strategy

    async def reason(
        self,
        request: UnderstandingRequest,
        context,
    ) -> UnderstandingResult:

        return await self._strategy.understand(
            request,
        )