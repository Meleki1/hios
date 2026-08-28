from __future__ import annotations

from abc import ABC

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.execution.contract import ExecutionResult
from hios.capabilities.outcome.models.outcome import Outcome


class OutcomeRequest(
    CapabilityRequest,
):

    execution: ExecutionResult


class OutcomeResult(
    CapabilityResult,
):

    outcome: Outcome


class OutcomeCapability(
    Capability[
        OutcomeRequest,
        OutcomeResult,
    ],
    ABC,
):
    pass