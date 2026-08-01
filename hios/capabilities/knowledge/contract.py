from __future__ import annotations

from abc import ABC

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult


class KnowledgeRequest(CapabilityRequest):
    """
    Request for the Knowledge capability.
    """

    pass


class KnowledgeResult(CapabilityResult):
    """
    Result produced by the Knowledge capability.
    """

    facts: list[str]


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
