from abc import ABC
from pydantic import Field
from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.pest_control.models.assessment import (
    PestAssessment,
)
from hios.capabilities.pest_control.models.recommendation import (
    PestRecommendation,
)
from hios.capabilities.pest_control.models.observation import (
    PestObservation,
)
from hios.capabilities.goals.contract.result import (
    GoalResult,
)
from hios.capabilities.planning.contract import (
    PlanResult,
)
from hios.capabilities.decision.contract import (
    DecisionResult,
)
from hios.capabilities.execution.contract import (
    ExecutionResult,
)
from hios.capabilities.outcome.contract import (
    OutcomeResult,
)
from hios.capabilities.reflection.contract import (
    ReflectionResult,
)
from hios.capabilities.learning.contract import (
    LearningResult,
)
from hios.runtime.context import RuntimeContext

from hios.capabilities.knowledge.contract import (
    KnowledgeCapability,
    KnowledgeRequest,
)

from hios.capabilities.understanding.contract import (
    UnderstandingCapability,
    UnderstandingRequest,
)
from hios.capabilities.pest_control.models.observation import (
    PestObservation,
)

from hios.capabilities.pest_control.models.assessment import (
    PestAssessment,
)
from hios.capabilities.goals.capability import (
    GoalCapability, GoalRequest
)
from hios.capabilities.planning.capability import (
    PlanningCapability,
)

from hios.capabilities.planning.contract import (
    PlanRequest,
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
from hios.capabilities.reflection.contract import (
    ReflectionRequest,
)
from hios.capabilities.reflection.contract import (
    ReflectionCapability,
)
from hios.capabilities.learning.contract import (
    LearningCapability,
)
from hios.capabilities.learning.contract import (
    LearningRequest,
)
from hios.capabilities.safety.contract.result import (
    SafetyGuidanceResult,
)
from hios.capabilities.safety.contract.request import (
    SafetyGuidanceRequest,
)
from hios.capabilities.safety.capability import SafetyGuidanceCapability
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis


class PestControlRequest(
    CapabilityRequest,
):

    subject_id: str

    home_id: str

    message: str

    observation: str | None = None

    image_diagnosis: ImageDiagnosis | None = None


class PestControlResult(
    CapabilityResult,
):
    observation: PestObservation | None = None
    assessment: PestAssessment | None = None
    safety_guidance: SafetyGuidanceResult | None = None
    goals: GoalResult | None = None
    plans: PlanResult | None = None
    decision: DecisionResult | None = None
    execution: ExecutionResult | None = None
    outcome: OutcomeResult | None = None
    reflection: ReflectionResult | None = None
    learning: LearningResult | None = None
    recommendations: list[PestRecommendation] = Field(
        default_factory=list,
    )




class PestControlCapability(
    Capability[
        PestControlRequest,
        PestControlResult,
    ],
    ABC,
):
    pass



class DefaultPestControlCapability(
    PestControlCapability,
):

    def __init__(
        self,
        knowledge: KnowledgeCapability,
        understanding: UnderstandingCapability,
        goals: GoalCapability,
        planning: PlanningCapability,
        decision: DecisionCapability,
        execution: ExecutionCapability,
        outcome: OutcomeCapability,
        reflection: ReflectionCapability,
        learning: LearningCapability,
        safety: SafetyGuidanceCapability,
    ):
        self._knowledge = knowledge
        self._understanding = understanding
        self._goals = goals
        self._planning = planning
        self._decision = decision
        self._execution = execution
        self._outcome = outcome
        self._reflection = reflection
        self._learning = learning
        self._safety = safety

    async def reason(
        self,
        request: PestControlRequest,
        context: RuntimeContext,
    ) -> PestControlResult:

        observation_description = (
            request.observation
            or request.message
        )

        evidence = []

        if request.image_diagnosis:
            for finding in request.image_diagnosis.findings:
                evidence.append(
                    finding.description
                )

            visual_findings = " ".join(
                finding.description
                for finding in request.image_diagnosis.findings
            )

            observation_description = (
                f"{observation_description} "
                f"Visual evidence: {visual_findings}"
            )

        observation = PestObservation(
            subject_id=request.subject_id,
            home_id=request.home_id,
            description=observation_description,
            evidence=evidence,
            source=(
                "image_diagnosis"
                if request.image_diagnosis
                else "conversation"
            ),
        )

        knowledge_result = (
            await self._knowledge.execute(
                KnowledgeRequest(
                    observation=observation.description,
                ),
                context,
            )
        )

        understanding_result = (
            await self._understanding.execute(
                UnderstandingRequest(
                    knowledge=knowledge_result,
                ),
                context,
            )
        )

        safety_guidance_result = await self._safety.execute(
            SafetyGuidanceRequest(
                understanding=understanding_result,
            ),
            context,
        )

        print("\n=== SAFETY GUIDANCE RESULT ===")
        print(safety_guidance_result)

        goal_result = await self._goals.execute(
            GoalRequest(
                understanding=understanding_result,
            ),
            context,
        )

        plan_result = await self._planning.execute(
            PlanRequest(
                goals=goal_result,
            ),
            context,
        )

        if not plan_result.plans:
            return PestControlResult(
                knowledge=knowledge_result,
                understanding=understanding_result,
                safety_guidance=safety_guidance_result,
                goals=goal_result,
                plans=plan_result,
            )

        decision_result = await self._decision.execute(
            DecisionRequest(
                plans=plan_result,
            ),
            context,
        )

        execution_result = await self._execution.execute(
            ExecutionRequest(
                decision=decision_result,
            ),
            context,
        )

        outcome_result = await self._outcome.execute(
            OutcomeRequest(
                execution=execution_result,
            ),
            context,
        )

        reflection_result = await self._reflection.execute(
            ReflectionRequest(
                outcome=outcome_result,
            ),
            context,
        )

        learning_result = await self._learning.execute(
            LearningRequest(
                reflection=reflection_result,
            ),
            context,
        )

        assessment = None

        if understanding_result.hypotheses:

            hypothesis = (
                understanding_result.hypotheses[0]
            )

            assessment = PestAssessment(
                observation_id=observation.id,
                pest_type=hypothesis.name,
                confidence=hypothesis.confidence,
                explanation=hypothesis.description,
                indicators=(
                    hypothesis.supporting_facts
                ),
            )

        return PestControlResult(
            observation=observation,
            assessment=assessment,
            goals=goal_result,
            plans=plan_result,
            decision=decision_result,
            execution=execution_result,
            outcome=outcome_result,
            reflection=reflection_result,
            learning=learning_result,
        )



