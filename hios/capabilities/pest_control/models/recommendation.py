from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class PestRecommendation(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    assessment_id: str

    title: str

    description: str

    priority: str = "normal"

    actions: list[str] = Field(
        default_factory=list,
    )