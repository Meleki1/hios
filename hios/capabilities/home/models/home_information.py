from pydantic import Field
from uuid import uuid4
from hios.shared.base import HIOSModel


class HomeInformation(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    home_id: str

    country: str

    city: str

    address: str

    postcode: str | None = None