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
import yaml
from hios.runtime.context import RuntimeContext


RULES_PATH = "hios/packs/pest_control/rules/"


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

@pytest.mark.asyncio
async def test_droppings_and_scratching_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and I can hear "
                "scratching in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts



@pytest.mark.asyncio
async def test_rodent_odor_produces_possible_rodent_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="There is a strange rodent-like odor in the kitchen.",
            evidence=[],
        ),
        None,
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_droppings_alone_do_not_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found droppings in the kitchen.",
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" not in result.facts

@pytest.mark.asyncio
async def test_droppings_and_scratching_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and I can hear "
                "scratching in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts

@pytest.mark.asyncio
async def test_droppings_and_odor_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and there is "
                "a strong odor in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts

@pytest.mark.asyncio
async def test_scratching_and_odor_produce_possible_rodent_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I hear scratching and notice "
                "a strange odor in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_droppings_scratching_and_odor_produce_severe_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings, hear scratching, "
                "and notice a strange odor."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts

@pytest.mark.asyncio
async def test_gnawing_produces_possible_rodent_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I noticed gnawing on a cabinet in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_rodent_sighting_produces_possible_rodent_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "There was a rodent sighting in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_nesting_material_produces_possible_rodent_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found nesting material in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_droppings_and_gnawing_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and noticed "
                "gnawing in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts

@pytest.mark.asyncio
async def test_droppings_and_rodent_sighting_produce_severe_rodent_infestation():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "There was a rodent sighting and "
                "I found droppings in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "High confidence infestation" in result.facts


@pytest.mark.asyncio
async def test_cockroach_sighting_produces_possible_cockroach_activity():
    repository = YamlRuleRepository(RULES_PATH)

    from pathlib import Path

    print("RULES_PATH:", RULES_PATH)
    print("RULES_PATH ABS:", Path(RULES_PATH).resolve())
    print("RULES_PATH EXISTS:", Path(RULES_PATH).exists())
    print(
        "YAML FILES:",
        list(Path(RULES_PATH).rglob("*.yaml")),
    )

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation=(
                "There was a cockroach sighting "
                "in the kitchen."
            ),
            evidence=[],
        ),
        None,
    )

    assert "Possible cockroach activity" in result.facts

@pytest.mark.asyncio
async def test_cockroach_droppings_produce_possible_cockroach_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found cockroach droppings in the kitchen.",
            evidence=[],
        ),
        None,
    )

    assert "Possible cockroach activity" in result.facts

@pytest.mark.asyncio
async def test_cockroach_egg_case_produces_possible_cockroach_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="I found an egg case in the kitchen.",
            evidence=[],
        ),
        None,
    )

    assert "Possible cockroach activity" in result.facts

@pytest.mark.asyncio
async def test_cockroach_musty_odor_produces_possible_cockroach_activity():
    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.execute(
        KnowledgeRequest(
            observation="There is a musty odor in the kitchen.",
            evidence=[],
        ),
        None,
    )

    assert "Possible cockroach activity" in result.facts

