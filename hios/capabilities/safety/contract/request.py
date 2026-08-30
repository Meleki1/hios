from hios.contracts.requests import CapabilityRequest
from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)


class SafetyGuidanceRequest(CapabilityRequest):
    understanding: UnderstandingResult