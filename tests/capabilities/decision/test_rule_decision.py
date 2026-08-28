from __future__ import annotations
import pytest
from hios.capabilities.decision.contract import DecisionRequest
from hios.capabilities.decision.rule import RuleDecisionCapability
from hios.capabilities.understanding.contract import UnderstandingResult
from hios.runtime.context import RuntimeContext


@pytest.mark.asyncio
async def test_rule_decision():

    request = DecisionRequest(
        understanding=UnderstandingResult(
            hypotheses=[
                "Possible rodent activity",
            ],
            reasoning=[
                "Mouse-related evidence detected.",
            ],
            confidence=0.90,
        )
    )

    capability = RuleDecisionCapability()

    result = await capability.execute(
        request,
        RuntimeContext(),
    )

    assert result.priority == "high"
    assert "Schedule a professional inspection." in result.recommendations