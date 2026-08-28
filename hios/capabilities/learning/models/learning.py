from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.learning.models.lesson import Lesson
from hios.capabilities.reflection.models.reflection import Reflection


class Learning(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    reflection: Reflection

    lessons: list[Lesson] = Field(
        default_factory=list,
    )

    summary: str = ""

    score: float = 0.0