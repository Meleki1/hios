from abc import ABC

from hios.contracts.capability import Capability

from hios.capabilities.planning.contract import (
    PlanRequest,
    PlanResult,
)


class PlanningCapability(
    Capability[
        PlanRequest,
        PlanResult,
    ],
    ABC,
):
    """
    Contract for planning capabilities.
    """

    pass