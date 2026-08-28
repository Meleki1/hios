from __future__ import annotations
from abc import ABC
from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from typing import Any
from hios.shared.base import HIOSModel


class InputData(HIOSModel):
    content: dict[str, Any]


class KnowledgeRequest(CapabilityRequest):
    observation: str


class KnowledgeResult(CapabilityResult):
   
    facts: list[str]


class KnowledgeCapability(
    Capability[
        KnowledgeRequest,
        KnowledgeResult,
    ],
    ABC,
):
 

    pass