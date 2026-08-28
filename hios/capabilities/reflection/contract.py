from __future__ import annotations

from abc import ABC

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.outcome.contract import OutcomeResult
from hios.capabilities.reflection.models.reflection import (
    Reflection,
)


class ReflectionRequest(
    CapabilityRequest,
):

    outcome: OutcomeResult


class ReflectionResult(
    CapabilityResult,
):

    reflection: Reflection


class ReflectionCapability(
    Capability[
        ReflectionRequest,
        ReflectionResult,
    ],
    ABC,
):
    pass