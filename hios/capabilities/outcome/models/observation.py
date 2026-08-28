from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class OutcomeObservation(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    action_id: str

    description: str