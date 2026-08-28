from hios.intelligence.models.rule import Rule
from tests.runtime.conftest import InMemoryRuleRepository
from hios.capabilities.knowledge.contract import KnowledgeRequest
from hios.capabilities.knowledge.rule import RuleKnowledgeCapability
import pytest
from hios.runtime.context import RuntimeContext


def test_create_rule():

    rule = Rule(
        id="rodent",
        name="Rodent Evidence",
        keywords=[
            "droppings",
            "pellets",
        ],
        facts=[
            "Possible rodent activity",
        ],
        confidence=0.95,
    )

    assert rule.id == "rodent"
    assert rule.enabled is True
    assert rule.confidence == 0.95
    assert rule.facts == [
        "Possible rodent activity",
    ]


from pathlib import Path

from hios.intelligence.repositories.yaml import (
    YamlRuleRepository,
)


def test_load_yaml_rules(tmp_path: Path):

    rule = tmp_path / "rule.yaml"

    rule.write_text(
        """
id: rodent

name: Rodent

keywords:
  - droppings

facts:
  - Rodent activity

confidence: 0.9
enabled: true
priority: 100
tags:
  - rodents
"""
    )

    repository = YamlRuleRepository(tmp_path)

    rules = repository.load()

    assert len(rules) == 1
    assert rules[0].id == "rodent"


from hios.intelligence.matchers.keyword import (
    KeywordRuleMatcher,
)
from hios.intelligence.models.rule import Rule


def test_keyword_rule_matches():

    matcher = KeywordRuleMatcher()

    rule = Rule(
        id="rodent",
        name="Rodent",
        keywords=[
            "droppings",
            "pellets",
        ],
        facts=[
            "Rodent activity",
        ],
    )

    assert matcher.matches(
        rule,
        "I found droppings under the sink.",
    )

@pytest.mark.asyncio
async def test_single_rule_matches():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Possible rodent activity"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found droppings."
        ),
        RuntimeContext()
    )

    assert result.facts == [
        "Possible rodent activity",
    ]

@pytest.mark.asyncio
async def test_no_matching_rules():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Possible rodent activity"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="Everything looks clean."
        )
    )

    assert result.facts == []

@pytest.mark.asyncio
async def test_multiple_rules_match():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Rodent evidence"],
            ),
            Rule(
                id="noise",
                name="Noise",
                keywords=["scratching"],
                facts=["Rodent movement"],
            ),
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="""
            I found droppings.
            I hear scratching.
            """
        )
    )

    assert len(result.facts) == 2

@pytest.mark.asyncio
async def test_disabled_rule_is_ignored():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                enabled=False,
                keywords=["droppings"],
                facts=["Should never appear"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="Droppings found."
        )
    )

    assert result.facts == []

@pytest.mark.asyncio
async def test_empty_repository():

    repository = InMemoryRuleRepository([])

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="Anything"
        )
    )

    assert result.facts == []

@pytest.mark.asyncio
async def test_empty_observation():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Rodent"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=""
        )
    )

    assert result.facts == []

@pytest.mark.asyncio
async def test_matching_is_case_insensitive():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Rodent"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="DROPPINGS"
        )
    )

    assert result.facts == [
        "Rodent",
    ]

class SpyRepository(InMemoryRuleRepository):

    def __init__(self, rules):
        super().__init__(rules)
        self.calls = 0

    def load(self):
        self.calls += 1
        return super().load()




@pytest.mark.asyncio
async def test_repository_loaded_once():

    repository = SpyRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Possible rodent activity"],
            )
        ]
    )

    matcher = KeywordRuleMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    await capability.execute(
        KnowledgeRequest(
            observation="I found droppings.",
        ),
        RuntimeContext(),
    )

    assert repository.calls == 1

class SpyMatcher(KeywordRuleMatcher):

    def __init__(self):
        self.calls = 0

    def matches(self, rule, text):
        self.calls += 1
        return super().matches(rule, text)

@pytest.mark.asyncio
async def test_matcher_called_for_every_enabled_rule():

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="r1",
                name="Rule 1",
                keywords=["a"],
                facts=["A"],
            ),
            Rule(
                id="r2",
                name="Rule 2",
                keywords=["b"],
                facts=["B"],
            ),
        ]
    )

    matcher = SpyMatcher()

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    await capability.execute(
        KnowledgeRequest(
            observation="a b",
        ),
        RuntimeContext(),
    )

    assert matcher.calls == 2


@pytest.fixture
def context():
    return RuntimeContext()


@pytest.fixture
def matcher():
    return KeywordRuleMatcher()

@pytest.mark.asyncio
async def test_single_rule_matches(context, matcher):

    repository = InMemoryRuleRepository(
        [
            Rule(
                id="rodent",
                name="Rodent",
                keywords=["droppings"],
                facts=["Possible rodent activity"],
            )
        ]
    )

    capability = RuleKnowledgeCapability(
        repository,
        matcher,
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found droppings.",
        ),
        context,
    )

    assert result.facts == [
        "Possible rodent activity",
    ]