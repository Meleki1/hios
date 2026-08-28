import pytest

from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
)
from hios.intelligence.evidence.model import Evidence
from hios.intelligence.evaluators.result import EvaluationResult
import pytest

from hios.capabilities.understanding.rule import (
    RuleUnderstandingCapability,
)


@pytest.fixture
def evaluation():

    return EvaluationResult(
        matched=True,
        score=1.0,
        matched_operands=[
            "droppings",
        ],
        unmatched_operands=[],
    )


@pytest.fixture
def evidence(evaluation):

    return Evidence(
        rule_id="rodent",
        rule_name="Rodent Evidence",
        evaluation=evaluation,
        observations=[
            "Droppings found.",
        ],
    )


def test_create_hypothesis(evidence):

    hypothesis = Hypothesis(
        id="rodent",
        name="Rodent Infestation",
        description="Evidence suggests rodent activity.",
        confidence=0.9,
        supporting_facts=[
            "Possible rodent activity",
        ],
        evidence=[
            evidence,
        ],
    )

    assert hypothesis.id == "rodent"
    assert hypothesis.name == "Rodent Infestation"
    assert hypothesis.confidence == 0.9


def test_supporting_facts(evidence):

    hypothesis = Hypothesis(
        id="rodent",
        name="Rodent Infestation",
        description="Evidence suggests rodent activity.",
        confidence=0.9,
        supporting_facts=[
            "Possible rodent activity",
            "Signs of nesting",
        ],
        evidence=[
            evidence,
        ],
    )

    assert len(hypothesis.supporting_facts) == 2


def test_hypothesis_preserves_evidence(evidence):

    hypothesis = Hypothesis(
        id="rodent",
        name="Rodent Infestation",
        description="Evidence suggests rodent activity.",
        confidence=0.9,
        supporting_facts=[],
        evidence=[
            evidence,
        ],
    )

    assert len(hypothesis.evidence) == 1
    assert hypothesis.evidence[0].rule_id == "rodent"

from hios.capabilities.understanding.models.assumption import (
    Assumption,
)


def test_create_assumption():

    assumption = Assumption(
        description="The infestation is active.",
        reason="Fresh droppings were observed.",
    )

    assert assumption.description == "The infestation is active."
    assert assumption.reason == "Fresh droppings were observed."

from hios.capabilities.understanding.models.unknown import (
    Unknown,
)


def test_create_unknown():

    unknown = Unknown(
        description="Species cannot be determined.",
    )

    assert unknown.description == "Species cannot be determined."

from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)
from hios.capabilities.understanding.models.assumption import (
    Assumption,
)
from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
)
from hios.capabilities.understanding.models.unknown import (
    Unknown,
)


def test_empty_understanding_result():

    result = UnderstandingResult()

    assert result.hypotheses == []
    assert result.assumptions == []
    assert result.unknowns == []


def test_multiple_hypotheses():

    result = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="1",
                name="Rodent",
                description="...",
                confidence=0.9,
                supporting_facts=[],
                evidence=[],
            ),
            Hypothesis(
                id="2",
                name="Cockroach",
                description="...",
                confidence=0.6,
                supporting_facts=[],
                evidence=[],
            ),
        ]
    )

    assert len(result.hypotheses) == 2


def test_unknowns():

    result = UnderstandingResult(
        unknowns=[
            Unknown(
                description="Species unknown.",
            )
        ]
    )

    assert len(result.unknowns) == 1


def test_assumptions():

    result = UnderstandingResult(
        assumptions=[
            Assumption(
                description="Infestation is active.",
                reason="Fresh evidence.",
            )
        ]
    )

    assert len(result.assumptions) == 1

from hios.capabilities.knowledge.contract import KnowledgeResult
from hios.capabilities.understanding.default import (
    RuleBasedHypothesisResolver,
)


def test_resolve_rodent_hypothesis():

    resolver = RuleBasedHypothesisResolver()

    knowledge = KnowledgeResult(
        facts=[
            "Possible rodent activity",
        ],
        evidence=[],
    )

    hypotheses = resolver.resolve(
        knowledge,
    )

    assert len(hypotheses) == 1
    assert hypotheses[0].name == "Rodent Infestation"


def test_no_matching_hypothesis():

    resolver = RuleBasedHypothesisResolver()

    knowledge = KnowledgeResult(
        facts=[],
        evidence=[],
    )

    hypotheses = resolver.resolve(
        knowledge,
    )

    assert hypotheses == []

from hios.capabilities.knowledge.contract import (
    KnowledgeResult,
)
from hios.capabilities.understanding.contract import (
    UnderstandingRequest,
)
from hios.capabilities.understanding.default import (
    DefaultUnderstandingStrategy,
    RuleBasedHypothesisResolver,
)


def test_strategy_generates_understanding():

    strategy = DefaultUnderstandingStrategy(
        RuleBasedHypothesisResolver(),
    )

    request = UnderstandingRequest(
        knowledge=KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    result = strategy.understand(
        request,
    )

    assert len(result.hypotheses) == 1
    assert result.hypotheses[0].name == "Rodent Infestation"


def test_strategy_handles_empty_knowledge():

    strategy = DefaultUnderstandingStrategy(
        RuleBasedHypothesisResolver(),
    )

    request = UnderstandingRequest(
        knowledge=KnowledgeResult(
            facts=[],
            evidence=[],
        )
    )

    result = strategy.understand(
        request,
    )

    assert result.hypotheses == []

@pytest.mark.asyncio
async def test_rule_understanding_capability_uses_strategy():

    strategy = DefaultUnderstandingStrategy(
        RuleBasedHypothesisResolver(),
    )

    capability = RuleUnderstandingCapability(
        strategy=strategy,
    )

    request = UnderstandingRequest(
        knowledge=KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert len(result.hypotheses) == 1

    assert (
        result.hypotheses[0].name
        == "Rodent Infestation"
    )

    assert (
        result.hypotheses[0].confidence
        == 0.9
    )