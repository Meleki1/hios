import pytest

from hios.capabilities.knowledge.contract import KnowledgeRequest
from hios.capabilities.knowledge.rule import RuleKnowledgeCapability
from hios.runtime.context import RuntimeContext


@pytest.mark.asyncio
async def test_rule_knowledge():

    capability = RuleKnowledgeCapability()

    result = await capability.execute(
        KnowledgeRequest(),
        RuntimeContext(),
    )

    assert result.facts == [
        "Knowledge acquired."
    ]