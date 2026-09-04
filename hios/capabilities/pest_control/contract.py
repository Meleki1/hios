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
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis
from hios.capabilities.safety.contract.result import SafetyGuidanceResult


class PestControlRequest(
    CapabilityRequest,
):

    subject_id: str

    home_id: str

    message: str

    observation: str | None = None

    image_diagnosis: ImageDiagnosis | None = None

    previously_communicated_guidance: list[str] = Field(
        default_factory=list,
    )


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


