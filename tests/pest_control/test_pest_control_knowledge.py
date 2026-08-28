import pytest

from hios.capabilities.knowledge.contract import (
    KnowledgeRequest,
)
from hios.capabilities.knowledge.rule import (
    RuleKnowledgeCapability,
)
from hios.intelligence.evaluators.rule import (
    RuleEvaluator,
)
from hios.intelligence.evidence.factory import (
    EvidenceFactory,
)
from hios.intelligence.repositories.yaml import (
    YamlRuleRepository,
)
from hios.runtime.context import RuntimeContext


RULES_PATH = "hios/packs/pest_control/rules"


@pytest.mark.asyncio
async def test_pest_control_rules_produce_knowledge():

    repository = YamlRuleRepository(
        RULES_PATH,
    )

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
        ),
        RuntimeContext(),
    )

    assert "Possible rodent activity" in result.facts

    assert "High confidence infestation" in result.facts

    assert len(result.evidence) == 2