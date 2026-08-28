from hios.runtime.context import RuntimeContext

from hios.capabilities.knowledge.contract import (
    KnowledgeCapability,
    KnowledgeRequest,
)

from hios.capabilities.understanding.contract import (
    UnderstandingCapability,
    UnderstandingRequest,
)

from hios.capabilities.pest_control.contract import (
    PestControlCapability,
    PestControlRequest,
    PestControlResult,
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

    async def reason(
        self,
        request: PestControlRequest,
        context: RuntimeContext,
    ) -> PestControlResult:

        evidence = []
        location = None

        if request.image_diagnosis:
            for finding in request.image_diagnosis.findings:
                evidence.append(finding.description)

                if finding.location and location is None:
                    location = finding.location

        observation_description = (
            request.observation
            or request.message
        )

        observation = PestObservation(
            subject_id=request.subject_id,
            home_id=request.home_id,
            description=observation_description,
            location=location,
            evidence=evidence,
            source=(
                "image_diagnosis"
                if request.image_diagnosis
                else "conversation"
            ),
        )
        print("\n=== BEFORE KNOWLEDGE ===")
        print("observation:", observation.description)
        print("observation.evidence:", observation.evidence)
        print("observation.location:", observation.location)

        knowledge_result = (
            await self._knowledge.execute(
                KnowledgeRequest(
                    observation=observation.description,
                    evidence=observation.evidence,
                ),
                context,
            )
        )

        print("\n=== KNOWLEDGE REQUEST ===")
        print("observation:", observation.description)
        print("evidence:", observation.evidence)

        print("\n=== KNOWLEDGE RESULT ===")
        print(knowledge_result)

        print("\n=== KNOWLEDGE RESULT ===")
        print(knowledge_result)

        understanding_result = (
            await self._understanding.execute(
                UnderstandingRequest(
                    knowledge=knowledge_result,
                ),
                context,
            )
        )

        print("\n=== UNDERSTANDING RESULT ===")
        print(understanding_result)

        goal_result = await self._goals.execute(
            GoalRequest(
                understanding=understanding_result,
            ),
            context,
        )

        print("\n=== GOAL RESULT ===")
        print(goal_result)

        plan_result = await self._planning.execute(
            PlanRequest(
                goals=goal_result,
            ),
            context,
        )

        print("\n=== PLAN RESULT ===")
        print(plan_result)

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
        print("\n=== DECISION RESULT ===")
        print(decision_result)

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
    def _build_observation(
        self,
        request: PestControlRequest,
    ) -> PestObservation:

        description = (
            request.observation
            or request.message
        )

        evidence: list[str] = []
        location: str | None = None

        if request.image_diagnosis:
            for finding in request.image_diagnosis.findings:
                evidence.append(finding.description)

                if finding.location and location is None:
                    location = finding.location

        if evidence:
            description = (
                f"{description}\n"
                + "\n".join(evidence)
            )

        source = (
            "combined"
            if request.message and request.image_diagnosis
            else (
                "image_diagnosis"
                if request.image_diagnosis
                else "conversation"
            )
        )

        return PestObservation(
            subject_id=request.subject_id,
            home_id=request.home_id,
            description=description,
            location=location,
            evidence=evidence,
            source=source,
        )