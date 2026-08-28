from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class HomePropertyReference(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    home_id: str

    uprn: str