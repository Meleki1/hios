from __future__ import annotations

from abc import ABC

from pydantic import Field

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.planning.contract import PlanResult
from hios.capabilities.decision.models.decision import Decision


class DecisionRequest(
    CapabilityRequest,
):

    plans: PlanResult


class DecisionResult(
    CapabilityResult,
):

    decision: Decision | None = None


class DecisionCapability(
    Capability[
        DecisionRequest,
        DecisionResult,
    ],
    ABC,
):
    pass