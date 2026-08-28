from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class Insight(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    category: str

    description: str

    score: float = 1.0