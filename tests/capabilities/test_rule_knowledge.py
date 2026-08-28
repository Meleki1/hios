import pytest

from hios.capabilities.knowledge.contract import KnowledgeRequest
from hios.capabilities.knowledge.rule import RuleKnowledgeCapability
from hios.runtime.context import RuntimeContext
from hios.capabilities.knowledge.rule import RuleKnowledgeCapability
from hios.capabilities.understanding.rule import RuleUnderstandingCapability
from hios.intelligence.evaluators.rule import (
    RuleEvaluator,
)
from hios.runtime.context import RuntimeContext

from hios.capabilities.knowledge.contract import (
    KnowledgeRequest,
)
from hios.intelligence.repositories.base import RuleRepository
from hios.intelligence.models.rule import Rule
from hios.intelligence.conditions.condition import Condition
from hios.intelligence.conditions.operator import ConditionOperator
from hios.intelligence.evidence.factory import EvidenceFactory


class InMemoryRuleRepository(
    RuleRepository,
):

    def __init__(
        self,
        rules: list[Rule],
    ):

        self._rules = rules

    def load(
        self,
    ) -> list[Rule]:

        return self._rules


@pytest.mark.asyncio
async def test_single_rule_matches():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                condition=Condition(
                    operator=ConditionOperator.ANY,
                    operands=[
                        "droppings",
                    ],
                ),
                facts=[
                    "Possible rodent activity",
                ],
            )
        ]
    )

    evaluator = RuleEvaluator()

    capability = RuleKnowledgeCapability(
        repository,
        evaluator,
        EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found droppings."
        ),
        RuntimeContext(),
    )

    assert result.facts == [
        "Possible rodent activity",
    ]

    assert len(result.evidence) == 1
    assert result.evidence[0]

@pytest.mark.asyncio
async def test_non_matching_condition_does_not_produce_facts():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                condition=Condition(
                    operator=ConditionOperator.ANY,
                    operands=[
                        "droppings",
                        "scratching",
                    ],
                ),
                facts=[
                    "Possible rodent activity",
                ],
            )
        ]
    )

    evaluator = RuleEvaluator()

    capability = RuleKnowledgeCapability(
        repository,
        evaluator,
        EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="Everything looks clean."
        ),
        RuntimeContext(),
    )

    assert result.facts == []
    assert result.evidence == []