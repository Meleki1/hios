from pydantic import Field

from hios.contracts.requests import CapabilityRequest


class PestControlRequest(CapabilityRequest):

    subject_id: str

    home_id: str

    message: str

    observation: str | None = None

    metadata: dict = Field(
        default_factory=dict,
    )
    
    previously_communicated_guidance: list[str] = Field(default_factory=list)