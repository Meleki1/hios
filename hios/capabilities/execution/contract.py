from __future__ import annotations

from abc import ABC

from hios.capabilities.decision.contract import DecisionResult
from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.capabilities.execution.models.execution import Execution

class ExecutionRequest(CapabilityRequest):
    """
    Input to the Execution capability.
    """

    decision: DecisionResult


class ExecutionResult(
    CapabilityResult,
):

    execution: Execution


class ExecutionCapability(
    Capability[
        ExecutionRequest,
        ExecutionResult,
    ],
    ABC,
):
    """
    Contract for execution providers.
    """

    pass