from pydantic import Field
from hios.shared.base import HIOSModel
from uuid import uuid4


class HomeState(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    home_id: str

    status: str = "active"