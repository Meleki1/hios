from pydantic import BaseModel, Field


class MaintenancePattern(BaseModel):
    category: str
    occurrences: int
    descriptions: list[str] = Field(
        default_factory=list,
    )
    confidence: float = 0.0