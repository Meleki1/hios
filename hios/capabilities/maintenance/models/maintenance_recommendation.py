from datetime import datetime

from pydantic import BaseModel, Field


class MaintenanceRecommendation(BaseModel):
    subject_id: str
    home_id: str

    task: str
    maintenance_type: str

    reason: str

    priority: str = "normal"

    recommended_for: datetime | None = None
    

    source_signals: list[str] = Field(
        default_factory=list,
    )

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )