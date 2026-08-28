from __future__ import annotations

from abc import ABC

from hios.contracts.capability import Capability

from hios.capabilities.decision.contract import (
    DecisionRequest,
    DecisionResult,
)


class DecisionCapability(
    Capability[
        DecisionRequest,
        DecisionResult,
    ],
    ABC,
):
    """
    Contract for decision capabilities.
    """

    pass