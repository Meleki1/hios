from hios.contracts.requests import CapabilityRequest
from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)
from pydantic import Field


class SafetyGuidanceRequest(CapabilityRequest):
    understanding: UnderstandingResult
    previously_communicated_guidance: list[str] = Field(default_factory=list)