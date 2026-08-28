from __future__ import annotations

from hios.capabilities.decision.contract import (
    DecisionCapability,
    DecisionRequest,
    DecisionResult,
)


class RuleDecisionCapability(
    DecisionCapability,
):

    async def reason(
        self,
        request: DecisionRequest,
        context,
    ) -> DecisionResult:

        hypotheses = " ".join(
            request.understanding.hypotheses
        ).lower()

        if "rodent" in hypotheses:

            return DecisionResult(
                recommendations=[
                    "Schedule a professional inspection.",
                    "Avoid disturbing the affected area.",
                ],
                priority="high",
            )

        return DecisionResult(
            recommendations=[
                "Gather additional evidence.",
            ],
            priority="low",
        )