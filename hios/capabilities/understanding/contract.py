from __future__ import annotations

from abc import ABC

from hios.capabilities.knowledge.contract import KnowledgeResult
from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from .models.hypothesis import Hypothesis
from .models.assumption import Assumption
from .models.unknown import Unknown
from pydantic import Field

class UnderstandingRequest(CapabilityRequest):
    
    knowledge: KnowledgeResult


class UnderstandingResult(CapabilityResult):

    hypotheses: list[Hypothesis] = Field(default_factory=list)
    assumptions: list[Assumption] = Field(default_factory=list)
    unknowns: list[Unknown] = Field(default_factory=list)


class UnderstandingCapability(
    Capability[
        UnderstandingRequest,
        UnderstandingResult,
    ],
    ABC,
):
    """
    Contract for understanding providers.
    """

    pass