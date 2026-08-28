from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class Lesson(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    category: str

    description: str

    confidence: float = 1.0