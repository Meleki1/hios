from pydantic import BaseModel, Field

from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)


class ImageDiagnosis(BaseModel):
    findings: list[ImageFinding] = Field(
        default_factory=list,
    )

    overall_confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )