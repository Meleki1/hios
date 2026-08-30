import pytest
from pathlib import Path
from hios.capabilities.knowledge.contract import (
    KnowledgeRequest,
    KnowledgeResult,
)
from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)
from hios.capabilities.safety.capability import (
    SafetyGuidanceCapability,
)

from hios.capabilities.safety.contract.request import (
    SafetyGuidanceRequest
)
from hios.capabilities.safety.contract.result import (
    SafetyGuidanceResult,
)
from hios.capabilities.safety.default import (
    DefaultSafetyGuidanceGenerator,
)

from hios.capabilities.safety.capability import (
    DefaultSafetyGuidanceCapability
)

from hios.capabilities.knowledge.rule import RuleKnowledgeCapability
from hios.capabilities.understanding.rule import RuleUnderstandingCapability

from hios.intelligence.repositories.yaml import (
    YamlRuleRepository,
)

from hios.intelligence.evaluators.rule import (
    RuleEvaluator,
)

from hios.runtime.context import RuntimeContext

from hios.capabilities.knowledge.contract import (
    KnowledgeRequest,
)

from hios.capabilities.pest_control.contract import (
    PestControlRequest,
)
from hios.capabilities.understanding.contract import (
    UnderstandingRequest,
    UnderstandingResult,
)

from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
)

from hios.capabilities.pest_control.contract import (
    PestControlRequest,
)

from hios.capabilities.pest_control.default_capability import (
    DefaultPestControlCapability,
)
from hios.capabilities.goals.contract.result import (
    GoalResult,
)

from hios.capabilities.goals.models.goal import (
    Goal,
)
from hios.capabilities.planning.contract import (
    PlanResult,
)

from hios.capabilities.planning.models.plan import (
    Plan,
)
from hios.capabilities.goals.models.priority import (
    GoalPriority,
)
from hios.capabilities.decision.contract import (
    DecisionResult,
)

from hios.capabilities.decision.models.decision import (
    Decision,
)

from hios.capabilities.execution.contract import (
    ExecutionResult,
)

from hios.capabilities.execution.models.execution import (
    Execution,
)

from hios.capabilities.outcome.contract import (
    OutcomeResult,
)
from hios.capabilities.outcome.models.outcome import (
    Outcome,
)

from hios.capabilities.outcome.models.status import (
    OutcomeStatus,
)
from hios.capabilities.reflection.contract import (
    ReflectionResult,
)

from hios.capabilities.reflection.models.reflection import (
    Reflection,
)
from hios.capabilities.reflection.models.insight import (
    Insight,
)
from hios.capabilities.learning.contract import LearningResult
from hios.capabilities.learning.models.learning import (
    Learning,
)
from hios.capabilities.learning.models.lesson import (
    Lesson,
)
from hios.intelligence.evidence.factory import EvidenceFactory
from hios.capabilities.understanding.default import DefaultUnderstandingStrategy, RuleBasedHypothesisResolver
from hios.capabilities.understanding.rule import RuleUnderstandingCapability
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
from hios.capabilities.execution.models.action import ActionType
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
from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)

from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.decision.contract import (
    DecisionRequest,
)
from hios.capabilities.decision.capability import (
    DecisionCapability,
)
from hios.capabilities.execution.capability import (
    ExecutionCapability, ExecutionRequest
)
from hios.capabilities.outcome.contract import (
    OutcomeCapability,
    OutcomeRequest,
)
from hios.capabilities.planning.models.task import Task
from tests.image_diagnosis.fakes import FakeImageDiagnosisProvider
from hios.capabilities.image_diagnosis.services.image_diagnosis_service import ImageDiagnosisService

class FakeSafetyGuidanceCapability(
    SafetyGuidanceCapability,
):
    def __init__(
        self,
        result: SafetyGuidanceResult,
    ):
        self.result = result
        self.request = None

    async def reason(
        self,
        request: SafetyGuidanceRequest,
        context,
    ) -> SafetyGuidanceResult:
        self.request = request
        return self.result

class FakeLearningCapability:

    def __init__(
        self,
        result: LearningResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> LearningResult:

        self.request = request

        return self.result

class FakeReflectionCapability:

    def __init__(
        self,
        result: ReflectionResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> ReflectionResult:

        self.request = request

        return self.result

class FakeOutcomeCapability:

    def __init__(
        self,
        result: OutcomeResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> OutcomeResult:

        self.request = request

        return self.result

class FakeExecutionCapability:

    def __init__(
        self,
        result: ExecutionResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> ExecutionResult:

        self.request = request

        return self.result

class FakeDecisionCapability:

    def __init__(
        self,
        result: DecisionResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> DecisionResult:

        self.request = request

        return self.result

class FakePlanningCapability:

    def __init__(
        self,
        result: PlanResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> PlanResult:

        self.request = request

        return self.result

class FakeGoalCapability:

    def __init__(
        self,
        result: GoalResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request,
        context,
    ) -> GoalResult:

        self.request = request

        return self.result


class FakeKnowledgeCapability:

    def __init__(
        self,
        result: KnowledgeResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request: KnowledgeRequest,
        context,
    ) -> KnowledgeResult:

        self.request = request

        return self.result


class FakeUnderstandingCapability:

    def __init__(
        self,
        result: UnderstandingResult,
    ):
        self.result = result
        self.request = None

    async def execute(
        self,
        request: UnderstandingRequest,
        context,
    ) -> UnderstandingResult:

        self.request = request

        return self.result
        
class FakeCapabilityThatShouldNotBeCalled:
    async def execute(
        self,
        request,
        context,
    ):
        raise AssertionError(
            "This capability should not be called "
            "when there is no executable plan."
        )

class FakeDecisionFromPlanCapability(
    DecisionCapability,
):
    def __init__(self):
        self.request = None
        self.result = None

    async def reason(
        self,
        request: DecisionRequest,
        context,
    ) -> DecisionResult:
        self.request = request

        plan = request.plans.plans[0]

        self.result = DecisionResult(
            decision=Decision(
                plan=plan,
                rationale=(
                    "Selected the available "
                    "evidence-gathering plan."
                ),
                score=1.0,
            )
        )

        return self.result

class FakeExecutionFromDecisionCapability(
    ExecutionCapability,
):
    def __init__(self):
        self.request = None
        self.result = None

    async def reason(
        self,
        request: ExecutionRequest,
        context,
    ) -> ExecutionResult:
        self.request = request

        self.result = ExecutionResult(
            execution=Execution(
                decision=request.decision.decision,
            )
        )

        return self.result

class FakeOutcomeFromExecutionCapability(
    OutcomeCapability,
):
    def __init__(self):
        self.request = None
        self.result = None

    async def reason(
        self,
        request: OutcomeRequest,
        context,
    ) -> OutcomeResult:
        self.request = request

        self.result = OutcomeResult(
            outcome=Outcome(
                execution=request.execution.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )

        return self.result

class FakeInvestigationCapability:

    def __init__(self, question):
        self.question = question
        self.request = None

    async def next_question(
        self,
        *,
        investigation_id: str,
        hypothesis_name: str | None = None,
    ):
        self.request = {
            "investigation_id": investigation_id,
            "hypothesis_name": hypothesis_name,
        }

        return self.question

@pytest.mark.asyncio
async def test_pest_control_capability_builds_assessment_from_understanding():

    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[],
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )
    planning = FakePlanningCapability(
        plans,
    )


    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )
    
    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
        safety=safety,
    )

    

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert result.observation is not None

    assert (
        result.observation.home_id
        == "home-123"
    )

    assert result.assessment is not None

    assert (
        result.assessment.observation_id
        == result.observation.id
    )

    assert (
        result.assessment.pest_type
        == "Rodent Infestation"
    )

    assert (
        result.assessment.confidence
        == 0.9
    )

    assert (
        result.assessment.indicators
        == [
            "Possible rodent activity",
        ]
    )
    assert (
        knowledge.request.observation
        == result.observation.description
    )

    assert (
        understanding.request.knowledge.facts
        == [
            "Possible rodent activity",
        ]
    )

@pytest.mark.asyncio
async def test_pest_control_capability_generates_goals_from_understanding():

    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )
    planning = FakePlanningCapability(
        plans,
    )


    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
        
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert result.goals is not None

    assert len(result.goals.goals) == 2

    assert (
        result.goals.goals[0].name
        == "Eliminate infestation"
    )

    assert (
        result.goals.goals[1].name
        == "Prevent recurrence"
    )

    assert (
        goals.request.understanding
        is understanding.result
    )


@pytest.mark.asyncio
async def test_pest_control_capability_passes_goals_to_planning():

    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )
    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert planning.request is not None

    assert (
        planning.request.goals
        is goals.result
    )

    assert result.plans is not None

    assert len(result.plans.plans) == 2

    assert (
        result.plans.plans[0].name
        == "Rodent Elimination Plan"
    )


@pytest.mark.asyncio
async def test_pest_control_capability_passes_plans_to_decision():

    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )

    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                    priority=GoalPriority.CRITICAL,
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                    priority=GoalPriority.HIGH,
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert decision.request is not None

    assert (
        decision.request.plans
        is planning.result
    )

    assert result.decision is not None

    assert (
        result.decision.decision.plan.name
        == "Rodent Elimination Plan"
    )

    assert (
        result.decision.decision.rationale
        == "Selected the highest priority plan."
    )


@pytest.mark.asyncio
async def test_pest_control_capability_passes_decision_to_execution():

    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                    priority=GoalPriority.CRITICAL,
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                    priority=GoalPriority.HIGH,
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert execution.request is not None

    assert (
        execution.request.decision
        is decision.result
    )

    assert result.execution is not None

    assert (
        result.execution.execution.decision
        == decision.result.decision
    )

@pytest.mark.asyncio
async def test_pest_control_capability_passes_execution_to_outcome():
    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                    priority=GoalPriority.CRITICAL,
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                    priority=GoalPriority.HIGH,
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )
    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert outcome.request is not None

    assert (
        outcome.request.execution
        is execution.result
    )

    assert result.outcome is not None

    assert (
        result.outcome.outcome.execution
        == execution.result.execution
    )

    assert (
        result.outcome.outcome.status
        == OutcomeStatus.SUCCESS
    )

@pytest.mark.asyncio
async def test_pest_control_capability_passes_outcome_to_reflection():
    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                    priority=GoalPriority.CRITICAL,
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                    priority=GoalPriority.HIGH,
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )
    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )
    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert reflection.request is not None

    assert (
        reflection.request.outcome
        is outcome.result
    )

    assert result.reflection is not None

    assert (
        result.reflection.reflection.outcome
        == outcome.result.outcome
    )

    assert (
        result.reflection.reflection.score
        == 1.0
    )

@pytest.mark.asyncio
async def test_pest_control_capability_passes_reflection_to_learning():
    knowledge = FakeKnowledgeCapability(
        KnowledgeResult(
            facts=[
                "Possible rodent activity",
            ],
            evidence=[],
        )
    )

    understanding = FakeUnderstandingCapability(
        UnderstandingResult(
            hypotheses=[
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence suggests "
                        "rodent activity."
                    ),
                    confidence=0.9,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=[],
                )
            ]
        )
    )
    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )
    goals = FakeGoalCapability(
        GoalResult(
            goals=[
                Goal(
                    id="eliminate_infestation",
                    name="Eliminate infestation",
                    description=(
                        "Remove the rodent infestation."
                    ),
                    priority=GoalPriority.CRITICAL,
                ),
                Goal(
                    id="prevent_recurrence",
                    name="Prevent recurrence",
                    description=(
                        "Prevent future infestations."
                    ),
                    priority=GoalPriority.HIGH,
                ),
            ]
        )
    )

    plans = PlanResult(
        plans=[
            Plan(
                goal_id="eliminate_infestation",
                name="Rodent Elimination Plan",
                description=(
                    "Eliminate the active "
                    "rodent infestation."
                ),
                priority=GoalPriority.CRITICAL,
            ),
            Plan(
                goal_id="prevent_recurrence",
                name="Rodent Prevention Plan",
                description=(
                    "Prevent future infestations."
                ),
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    planning = FakePlanningCapability(
        plans,
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=plans.plans[0],
                rationale=(
                    "Selected the highest "
                    "priority plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )
    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )
    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[
                    Insight(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary=(
                    "Execution completed successfully."
                ),
                score=1.0,
            )
        )
    )
    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[
                    Lesson(
                        category="success",
                        description=(
                            "Execution completed successfully."
                        ),
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )
    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )
    result = await capability.reason(
        request=request,
        context=None,
    )

    assert learning.request is not None

    assert (
        learning.request.reflection
        is reflection.result
    )

    assert result.learning is not None

    assert (
        result.learning.learning.reflection
        == reflection.result.reflection
    )

    assert len(
        result.learning.learning.lessons
    ) == 1

    assert (
        result.learning.learning.lessons[0].category
        == "success"
    )


RULES_PATH = (
        Path(__file__).resolve().parents[2]
        / "hios"
        / "packs"
        / "pest_control"
        / "rules"
    )


@pytest.mark.asyncio
async def test_pest_control_real_rules_produce_knowledge():

    

    repository = YamlRuleRepository(
        RULES_PATH
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await knowledge.execute(
        KnowledgeRequest(
            observation=(
                "I found droppings and "
                "hear scratching around my kitchen."
            )
        ),
        RuntimeContext(),
    )

    assert "Possible rodent activity" in result.facts
    assert "High confidence infestation" in result.facts


@pytest.mark.asyncio
async def test_pest_control_capability_uses_real_knowledge():

    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        )
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )

    # Keep the rest of the pipeline fake.
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
    

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
        ),
        RuntimeContext(),
    )

    assert result.observation is not None
    assert result.assessment is not None

    assert result.assessment.pest_type == (
        "Rodent Infestation"
    )

    assert result.assessment.confidence == 0.9

    assert (
        "Possible rodent activity"
        in result.assessment.indicators
    )
    assert result.goals is not None

    assert len(result.goals.goals) == 2

    assert result.goals.goals[0].id == (
        "eliminate_infestation"
    )

    assert result.goals.goals[1].id == (
        "prevent_recurrence"
    )
    assert all(
        goal.source_hypothesis == "rodent"
        for goal in result.goals.goals
    )
    assert (
        result.goals.goals[0].priority
        == GoalPriority.CRITICAL
    )

    assert (
        result.goals.goals[1].priority
        == GoalPriority.HIGH
    )
    assert result.plans is not None

    assert len(result.plans.plans) == 2

    assert (
        result.plans.plans[0].name
        == "Rodent Elimination Plan"
    )

    assert (
        result.plans.plans[1].name
        == "Rodent Prevention Plan"
    )
    assert (
        result.plans.plans[0].goal_id
        == "eliminate_infestation"
    )

    assert (
        result.plans.plans[1].goal_id
        == "prevent_recurrence"
    )
    assert (
        result.plans.plans[0].priority
        == GoalPriority.CRITICAL
    )

    assert (
        result.plans.plans[1].priority
        == GoalPriority.HIGH
    )
    assert result.decision is not None

    assert result.decision.decision is not None

    assert (
        result.decision.decision.plan.name
        == "Rodent Elimination Plan"
    )

    assert (
        result.decision.decision.plan.goal_id
        == "eliminate_infestation"
    )

    assert (
        result.decision.decision.rationale
        == "Selected the highest priority plan."
    )

    assert result.decision.decision.score == 1.0
    assert result.execution is not None

    assert result.execution.execution is not None

    assert (
        result.execution.execution.decision.plan.name
        == "Rodent Elimination Plan"
    )

    assert len(
        result.execution.execution.actions
    ) == 4
    assert (
    result.execution.execution.actions[0].name
    == "Inspect property"
)

    assert (
        result.execution.execution.actions[1].name
        == "Seal entry points"
    )

    assert (
        result.execution.execution.actions[2].name
        == "Deploy traps"
    )

    assert (
        result.execution.execution.actions[3].name
        == "Schedule follow-up"
    )
    assert result.execution is not None

    assert result.execution.execution is not None

    assert (
        result.execution.execution.decision.plan.name
        == "Rodent Elimination Plan"
    )

    assert len(
        result.execution.execution.actions
    ) == 4
    assert result.outcome is not None

    assert result.outcome.outcome is not None

    assert (
        result.outcome.outcome.status
        == OutcomeStatus.UNKNOWN
    )
    assert (
        result.outcome.outcome.execution
        == result.execution.execution
    )
    assert result.reflection is not None

    assert result.reflection.reflection is not None

    assert (
        result.reflection.reflection.outcome.status
        == OutcomeStatus.UNKNOWN
    )
    assert (
        result.reflection.reflection.score
        == 0.0
    )
    assert (
        result.reflection.reflection.insights[0].category
        == "failure"
    )
    assert (
        result.reflection.reflection.summary
        == "Execution failed."
    )

    assert result.learning is not None

    assert result.learning.learning is not None

    assert (
        result.learning.learning.summary
        == "Execution failed."
    )

    assert result.learning.learning.score == 0.0

    assert len(
        result.learning.learning.lessons
    ) == 1

    assert (
        result.learning.learning.lessons[0].category
        == "failure"
    )

    assert (
        result.learning.learning.lessons[0].description
        == "Execution failed."
    )
    assert (
        result.learning.learning.reflection
        == result.reflection.reflection
    )

@pytest.mark.asyncio
async def test_pest_control_capability_uses_image_diagnosis():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == "image_diagnosis"

    assert result.observation.description == (
        "I found droppings and hear scratching around my kitchen."
    )

    assert (
        "Possible rodent evidence."
        in result.observation.evidence
    )

@pytest.mark.asyncio
async def test_image_diagnosis_evidence_reaches_understanding():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )


    assert result.assessment is not None

    assert result.assessment.pest_type == (
        "Rodent Infestation"
    )

    assert result.assessment.confidence == 0.9

    assert (
        "Possible rodent activity"
        in result.assessment.indicators
    )

@pytest.mark.asyncio
async def test_pest_control_preserves_multiple_image_findings():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
            ImageFinding(
                category="entry_point",
                description="Possible entry point near the kitchen wall.",
                confidence=0.87,
                location="kitchen wall",
            ),
        ],
        overall_confidence=0.89,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and hear scratching "
                "around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == "image_diagnosis"

    assert (
        "Possible rodent evidence."
        in result.observation.evidence
    )

    assert (
        "Possible entry point near the kitchen wall."
        in result.observation.evidence
    )

    assert len(result.observation.evidence) == 2

@pytest.mark.asyncio
async def test_image_diagnosis_populates_observation_location():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == (
        "image_diagnosis"
    )

    assert result.observation.location == (
        "kitchen"
    )

@pytest.mark.asyncio
async def test_image_diagnosis_preserves_all_finding_evidence():
    
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
            ImageFinding(
                category="pest",
                description="Possible entry point near cabinet.",
                confidence=0.84,
                location="kitchen",
            ),
        ],
        overall_confidence=0.88,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == (
        "image_diagnosis"
    )

    assert (
        "Possible rodent evidence."
        in result.observation.evidence
    )

    assert (
        "Possible entry point near cabinet."
        in result.observation.evidence
    )

@pytest.mark.asyncio
async def test_image_diagnosis_confidence_reaches_pest_assessment():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None
    assert result.assessment is not None

    assert result.assessment.confidence == 0.9

@pytest.mark.asyncio
async def test_image_diagnosis_influences_pest_assessment():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.assessment is not None

    assert result.assessment.pest_type == (
        "Rodent Infestation"
    )

@pytest.mark.asyncio
async def test_empty_image_diagnosis_produces_no_image_evidence():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
            image_diagnosis=diagnosis,
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == (
        "image_diagnosis"
    )

    assert result.observation.evidence == []

@pytest.mark.asyncio
async def test_pest_control_without_image_diagnosis_remains_conversation():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )


    result = await capability.reason(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
        ),
        RuntimeContext(),
    )

    assert result.observation is not None

    assert result.observation.source == (
        "conversation"
    )

    assert result.observation.evidence == []

    assert result.observation.location is None

    assert result.assessment is not None

    assert result.assessment.pest_type == (
        "Rodent Infestation"
    )

@pytest.mark.asyncio
async def test_image_evidence_enriches_conversation_observation():
    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I hear scratching around "
            "my kitchen."
        ),
        image_diagnosis=diagnosis,
    )

    observation = capability._build_observation(request)

    # ---------------------------------------------------------
    # DEBUG OUTPUT
    # ---------------------------------------------------------

    print("\n=== ENRICHED OBSERVATION ===")

    print("description:")
    print(observation.description)

    print("\nlocation:")
    print(observation.location)

    print("\nevidence:")
    print(observation.evidence)

    print("\nsource:")
    print(observation.source)

    # ---------------------------------------------------------
    # ASSERTIONS
    # ---------------------------------------------------------

    assert observation.source == "combined"

    assert observation.description == (
        "I hear scratching around my kitchen.\n"
        "Possible rodent evidence."
    )

    assert observation.location == "kitchen"

    assert (
        "Possible rodent evidence."
        in observation.evidence
    )

@pytest.mark.asyncio
async def test_scratching_produces_possible_rodent_activity():

    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.reason(
        KnowledgeRequest(
            observation="I hear scratching around my kitchen.",
        ),
        RuntimeContext(),
    )

    assert "Possible rodent activity" in result.facts

@pytest.mark.asyncio
async def test_unrelated_observation_produces_no_rodent_knowledge():

    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.reason(
        KnowledgeRequest(
            observation="The kitchen light is flickering.",
        ),
        RuntimeContext(),
    )

    assert "Possible rodent activity" not in result.facts
    assert "High confidence infestation" not in result.facts

@pytest.mark.asyncio
async def test_droppings_and_scratching_produce_high_confidence_infestation():

    repository = YamlRuleRepository(RULES_PATH)

    capability = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    result = await capability.reason(
        KnowledgeRequest(
            observation=(
                "I found droppings in my kitchen "
                "and I hear scratching."
            ),
        ),
        RuntimeContext(),
    )

    assert "High confidence infestation" in result.facts

@pytest.mark.asyncio
async def test_pest_control_returns_safety_and_investigation_plan():
    # arrange knowledge + understanding...

    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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


    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing signs of rodents "
            "around my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert safety.request is not None

    assert result.safety_guidance is not None
    assert result.safety_guidance.guidance == [
        "Keep the affected area clear.",
    ]

    assert result.goals is not None
    assert len(result.goals.goals) == 1

    goal = result.goals.goals[0]

    assert goal.id == "investigate_issue"
    assert goal.name == "Understand the reported issue"

    assert result.plans is not None
    assert len(result.plans.plans) == 1

    assert (
        result.plans.plans[0].goal_id
        == "investigate_issue"
    )

    assert (
        result.plans.plans[0].name
        == "Investigate Reported Issue"
    )
    assert result.execution is not None
    assert result.execution.execution.actions

    action = result.execution.execution.actions[0]

    assert action.name == "Gather more information"
    assert action.action_type == ActionType.USER_INPUT

    assert result.outcome is None
    assert result.reflection is None
    assert result.learning is None

@pytest.mark.asyncio
async def test_scratching_produces_safety_and_evidence_plan():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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
    outcome = FakeCapabilityThatShouldNotBeCalled()
    reflection = FakeCapabilityThatShouldNotBeCalled()
    learning = FakeCapabilityThatShouldNotBeCalled()

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="I can hear scratching in my kitchen.",
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert result.safety_guidance is not None
    assert result.safety_guidance.guidance == [
        "Keep the affected area clear.",
    ]

    assert result.goals is not None
    assert len(result.goals.goals) == 1

    goal = result.goals.goals[0]

    assert goal.id == "investigate_rodent_activity"
    assert goal.name == "Gather visual evidence"
    assert goal.source_hypothesis == "rodent"

    assert result.plans is not None
    assert len(result.plans.plans) == 1

    plan = result.plans.plans[0]

    assert plan.goal_id == "investigate_rodent_activity"
    assert plan.name == "Gather Visual Evidence"

    assert len(plan.tasks) == 1
    assert plan.tasks[0].name == "Request Image Evidence"
    assert plan.tasks[0].required is True
    assert result.decision is not None
    assert result.decision.decision is not None

    assert result.decision.decision.plan.id == plan.id

    assert result.execution is not None
    assert result.execution.execution is not None
    assert result.execution.execution.actions
    assert any(
        action.action_type == ActionType.IMAGE_REQUEST
        for action in result.execution.execution.actions
    )


@pytest.mark.asyncio
async def test_pest_control_turns_unknown_issue_into_investigation_plan():
    repository = YamlRuleRepository(
        RULES_PATH,
    )

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )

    goals = DefaultGoalCapability(
        generator=DefaultGoalGenerator(),
    )

    planning = DefaultPlanningCapability(
        planner=DefaultPlanner(),
    )

    investigation_plan = Plan(
        goal_id="investigate_issue",
        name="Investigate Reported Issue",
        description=(
            "Gather additional information to better "
            "understand the reported issue."
        ),
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Gather more information",
                description=(
                    "Ask targeted questions to better "
                    "understand the reported issue."
                ),
                required=True,
            )
        ],
    )

    decision = FakeDecisionCapability(
        DecisionResult(
            decision=Decision(
                plan=investigation_plan,
                rationale=(
                    "Selected the investigation plan."
                ),
                score=1.0,
            )
        )
    )

    execution = FakeExecutionCapability(
        ExecutionResult(
            execution=Execution(
                decision=decision.result.decision,
            )
        )
    )

    outcome = FakeOutcomeCapability(
        OutcomeResult(
            outcome=Outcome(
                execution=execution.result.execution,
                status=OutcomeStatus.SUCCESS,
            )
        )
    )

    reflection = FakeReflectionCapability(
        ReflectionResult(
            reflection=Reflection(
                outcome=outcome.result.outcome,
                insights=[],
                summary="Investigation plan selected.",
                score=1.0,
            )
        )
    )

    learning = FakeLearningCapability(
        LearningResult(
            learning=Learning(
                reflection=reflection.result.reflection,
                lessons=[],
                summary="Investigation plan selected.",
                score=1.0,
            )
        )
    )

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "There is something strange happening "
            "in my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert result.safety_guidance is not None

    assert result.goals is not None
    assert len(result.goals.goals) == 1

    goal = result.goals.goals[0]

    assert goal.id == "investigate_issue"
    assert goal.name == "Understand the reported issue"
    assert goal.priority == GoalPriority.HIGH
    assert goal.source_hypothesis is None

    assert result.plans is not None
    assert len(result.plans.plans) == 1

    plan = result.plans.plans[0]

    assert plan.goal_id == "investigate_issue"
    assert plan.name == "Investigate Reported Issue"
    assert plan.priority == GoalPriority.HIGH

    assert len(plan.tasks) >= 1

@pytest.mark.asyncio
async def test_pest_control_does_not_repeat_unchanged_safety_guidance():
    context = RuntimeContext()

    understanding = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="rodent",
                name="Possible Rodent Activity",
                description=(
                    "Evidence suggests possible rodent activity."
                ),
                confidence=0.7,
                supporting_facts=[
                    "Possible rodent activity",
                ],
                evidence=[],
            )
        ]
    )

    safety = DefaultSafetyGuidanceCapability(
        generator=DefaultSafetyGuidanceGenerator(),
    )

    request = SafetyGuidanceRequest(
        understanding=understanding,
    )

    first = await safety.reason(
        request=request,
        context=context,
    )

    assert first.guidance

    second = await safety.reason(
        request=request,
        context=context,
    )

    assert second.guidance == []

@pytest.mark.asyncio
async def test_pest_control_returns_new_safety_guidance_when_risk_changes():
    context = RuntimeContext()

    safety = DefaultSafetyGuidanceCapability(
        generator=DefaultSafetyGuidanceGenerator(),
    )

    possible_rodent = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="rodent",
                name="Possible Rodent Activity",
                description=(
                    "Evidence suggests possible rodent activity."
                ),
                confidence=0.7,
                supporting_facts=[
                    "Possible rodent activity",
                ],
                evidence=[],
            )
        ]
    )

    first = await safety.reason(
        request=SafetyGuidanceRequest(
            understanding=possible_rodent,
        ),
        context=context,
    )

    assert first.guidance == [
        "Avoid handling suspected rodent droppings or contaminated material with bare hands.",
        "Keep the affected area clear while the source of the activity is being investigated.",
    ]

    confirmed_rodent = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="rodent-infestation",
                name="Rodent Infestation",
                description=(
                    "Evidence suggests an active rodent infestation."
                ),
                confidence=0.9,
                supporting_facts=[
                    "Rodent infestation",
                ],
                evidence=[],
            )
        ]
    )

    second = await safety.reason(
        request=SafetyGuidanceRequest(
            understanding=confirmed_rodent,
        ),
        context=context,
    )

    assert second.guidance == [
        "Avoid direct contact with rodents or suspected contaminated material.",
        "Keep children and pets away from areas showing signs of infestation.",
    ]

@pytest.mark.asyncio
async def test_pest_control_uses_investigation_for_unknown_issue():
    investigation = FakeInvestigationCapability(
        InvestigationQuestion(
            key="issue_location",
            question="Where exactly are you noticing the issue?",
            purpose="Determine the affected location.",
        )
    )

    repository = YamlRuleRepository(RULES_PATH)

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
    )

    goals = DefaultGoalCapability(
        generator=DefaultGoalGenerator(),
    )

    planning = DefaultPlanningCapability(
        planner=DefaultPlanner(),
    )

    investigation_plan = Plan(
        goal_id="investigate_issue",
        name="Investigate Reported Issue",
        description=(
            "Gather additional information to better "
            "understand the reported issue."
        ),
        priority=GoalPriority.HIGH,
        tasks=[
            Task(
                name="Ask Investigation Question",
                description=(
                    "Where exactly are you noticing the issue?"
                ),
                required=True,
            )
        ],
    )

    decision = DefaultDecisionCapability(
        selector=DefaultDecisionSelector(),
    )

    execution = DefaultExecutionCapability(
        executor=DefaultExecutor(),
    )

    outcome = FakeCapabilityThatShouldNotBeCalled()
    reflection = FakeCapabilityThatShouldNotBeCalled()
    learning = FakeCapabilityThatShouldNotBeCalled()

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        investigation=investigation,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "There is something strange happening "
            "in my kitchen."
        ),
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    # Investigation was actually consulted.
    assert investigation.request is not None

    assert investigation.request["investigation_id"] == (
        result.observation.id
    )

    # No hypothesis was available.
    assert investigation.request["hypothesis_name"] is None

    # Safety is still provided.
    assert result.safety_guidance is not None
    assert result.safety_guidance.guidance == [
        "Keep the affected area clear.",
    ]

    # Generic investigation goal.
    assert result.goals is not None
    assert len(result.goals.goals) == 1

    goal = result.goals.goals[0]

    assert goal.id == "investigate_issue"
    assert goal.name == "Understand the reported issue"

    # Investigation plan.
    assert result.plans is not None
    assert len(result.plans.plans) == 1

    plan = result.plans.plans[0]

    assert plan.goal_id == "investigate_issue"
    assert plan.name == "Investigate Reported Issue"

    assert len(plan.tasks) == 1

    task = plan.tasks[0]

    assert task.name == "Ask Investigation Question"
    assert task.description == (
        "Where exactly are you noticing the issue?"
    )
    assert task.required is True

    # The system asks for one thing and waits.
    assert result.execution is not None

    actions = result.execution.execution.actions

    assert len(actions) == 1

    assert actions[0].action_type == ActionType.USER_INPUT
    assert actions[0].description == (
        "Where exactly are you noticing the issue?"
    )

    assert result.outcome is None
    assert result.reflection is None
    assert result.learning is None


@pytest.mark.asyncio
async def test_pest_control_uses_specialized_rodent_evidence_plan():
    investigation = FakeInvestigationCapability(
        InvestigationQuestion(
            key="issue_location",
            question="Where exactly are you noticing the issue?",
            purpose="Determine the affected location.",
        )
    )

    repository = YamlRuleRepository(RULES_PATH)

    knowledge = RuleKnowledgeCapability(
        repository=repository,
        evaluator=RuleEvaluator(),
        evidence_factory=EvidenceFactory(),
    )

    understanding = RuleUnderstandingCapability(
        strategy=DefaultUnderstandingStrategy(
            resolver=RuleBasedHypothesisResolver(),
        ),
    )

    safety = FakeSafetyGuidanceCapability(
        SafetyGuidanceResult(
            guidance=[
                "Keep the affected area clear.",
            ],
        )
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

    outcome = FakeCapabilityThatShouldNotBeCalled()
    reflection = FakeCapabilityThatShouldNotBeCalled()
    learning = FakeCapabilityThatShouldNotBeCalled()

    capability = DefaultPestControlCapability(
        knowledge=knowledge,
        understanding=understanding,
        safety=safety,
        investigation=investigation,
        goals=goals,
        planning=planning,
        decision=decision,
        execution=execution,
        outcome=outcome,
        reflection=reflection,
        learning=learning,
    )

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="I can hear scratching in my kitchen.",
    )

    result = await capability.reason(
        request=request,
        context=None,
    )

    assert result.goals is not None
    assert len(result.goals.goals) == 1

    goal = result.goals.goals[0]

    assert goal.id == "investigate_rodent_activity"
    assert goal.name == "Gather visual evidence"
    assert goal.source_hypothesis == "rodent"
    assert result.plans is not None
    assert len(result.plans.plans) == 1

    plan = result.plans.plans[0]

    assert plan.goal_id == "investigate_rodent_activity"
    assert plan.name == "Gather Visual Evidence"

    assert len(plan.tasks) == 1
    assert plan.tasks[0].name == "Request Image Evidence"
    assert result.execution is not None

    actions = result.execution.execution.actions

    assert len(actions) == 1

    assert actions[0].action_type == ActionType.IMAGE_REQUEST