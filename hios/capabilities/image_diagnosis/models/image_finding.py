from pydantic import BaseModel, Field


class ImageFinding(BaseModel):
    category: str
    description: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    location: str | None = None

    metadata: dict[str, object] = Field(
        default_factory=dict,
        json_schema_extra={
            "additionalProperties": False,
        },
    )