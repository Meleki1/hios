from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)

from hios.contracts.requests import CapabilityRequest


class GoalRequest(CapabilityRequest):

    understanding: UnderstandingResult