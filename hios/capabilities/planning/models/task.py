from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class Task(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str

    description: str

    required: bool = True