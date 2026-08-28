from pydantic import Field

from hios.shared.base import HIOSModel


class InteractionUnderstanding(HIOSModel):

    explicit_intents: list[str] = Field(
        default_factory=list,
    )