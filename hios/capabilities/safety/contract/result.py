from pydantic import Field

from hios.contracts.results import CapabilityResult


class SafetyGuidanceResult(CapabilityResult):
    guidance: list[str] = Field(
        default_factory=list,
    )