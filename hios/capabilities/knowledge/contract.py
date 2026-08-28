from __future__ import annotations

from abc import ABC
from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from typing import Any
from hios.shared.base import HIOSModel
from hios.intelligence.evidence.model import Evidence
from pydantic import Field

class InputData(HIOSModel):
    content: dict[str, Any]


class KnowledgeRequest(CapabilityRequest):
    observation: str
    evidence: list[str] = Field(default_factory=list)


class KnowledgeResult(CapabilityResult):
    facts: list[str]

    evidence: list[Evidence]




class KnowledgeCapability(
    Capability[
        KnowledgeRequest,
        KnowledgeResult,
    ],
    ABC,
):
    """
    Base contract for all knowledge providers.
    """

    pass
