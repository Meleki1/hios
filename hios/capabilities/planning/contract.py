from __future__ import annotations
from pydantic import Field
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.planning.models.plan import Plan


class PlanRequest(CapabilityRequest):

    goals: GoalResult


class PlanResult(CapabilityResult):

    plans: list[Plan] = Field(
        default_factory=list
    )