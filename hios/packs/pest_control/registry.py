from pathlib import Path

from hios.runtime.types import CapabilityType

from hios.capabilities.pest_control.default_capability import (
    DefaultPestControlCapability,
)
from hios.capabilities.understanding.llm import LLMUnderstandingStrategy
from hios.capabilities.knowledge.rule import (
    RuleKnowledgeCapability,
)
from hios.capabilities.understanding.rule import (
    RuleUnderstandingCapability,
)
from hios.capabilities.understanding.default import DefaultUnderstandingStrategy, RuleBasedHypothesisResolver

from hios.capabilities.goals.capability import DefaultGoalCapability
from hios.capabilities.goals.default import DefaultGoalGenerator

from hios.capabilities.planning.default_capability import (
    DefaultPlanningCapability,
)
from hios.capabilities.planning.default_planner import (
    DefaultPlanner,
)

from hios.capabilities.decision.default_capability import (
    DefaultDecisionCapability,
)
from hios.capabilities.decision.default import (
    DefaultDecisionSelector,
)

from hios.capabilities.execution.default_capability import (
    DefaultExecutionCapability,
)
from hios.capabilities.execution.default import (
    DefaultExecutor,
)

from hios.capabilities.outcome.default_capability import (
    DefaultOutcomeCapability,
)
from hios.capabilities.outcome.default import (
    DefaultOutcomeEvaluator,
)

from hios.capabilities.reflection.default_capability import (
    DefaultReflectionCapability,
)
from hios.capabilities.reflection.default import (
    DefaultReflector,
)

from hios.capabilities.learning.default_capability import (
    DefaultLearningCapability,
)
from hios.capabilities.learning.default import (
    DefaultLearner,
)

from hios.intelligence.evaluators.rule import RuleEvaluator
from hios.intelligence.evidence.factory import EvidenceFactory

from hios.intelligence.repositories.yaml import (
    YamlRuleRepository,
)
from hios.capabilities.safety.capability import (
    DefaultSafetyGuidanceCapability,
)

from hios.capabilities.safety.llm import LLMSafetyGuidanceGenerator


RULES_PATH = Path(__file__).parent / "rules"


def register(builder, *, llm):

    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=LLMUnderstandingStrategy(llm=llm),
    )

    safety = DefaultSafetyGuidanceCapability(
        generator=LLMSafetyGuidanceGenerator(llm=llm),
    )

    goals = DefaultGoalCapability(
        generator=DefaultGoalGenerator(),
    )

    planning = DefaultPlanningCapability(
        planner=DefaultPlanner(),
    )

    decision = DefaultDecisionCapability(
        selector=DefaultDecisionSelector(),
    )

    execution = DefaultExecutionCapability(
        executor=DefaultExecutor(),
    )

    outcome = DefaultOutcomeCapability(
        evaluator=DefaultOutcomeEvaluator(),
    )

    reflection = DefaultReflectionCapability(
        reflector=DefaultReflector(),
    )

    learning = DefaultLearningCapability(
        learner=DefaultLearner(),
    )

    pest_control = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        goals=goals,
        safety=safety,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    builder.register(
        CapabilityType.PEST_CONTROL,
        pest_control,
    )