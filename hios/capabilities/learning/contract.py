from __future__ import annotations

from abc import ABC

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult

from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.reflection.contract import ReflectionResult


class LearningRequest(
    CapabilityRequest,
):

    reflection: ReflectionResult


class LearningResult(
    CapabilityResult,
):

    learning: Learning


class LearningCapability(
    Capability[
        LearningRequest,
        LearningResult,
    ],
    ABC,
):
    pass