from pydantic import Field
from uuid import uuid4
from hios.shared.base import HIOSModel


class Home(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str

    home_type: str

    description: str | None = None

    status: str = "active"

    