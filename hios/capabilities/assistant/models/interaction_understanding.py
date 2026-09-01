from pydantic import BaseModel, Field
from enum import Enum
from hios.shared.base import HIOSModel

class InteractionType(str, Enum):
    NEW_REQUEST = "new_request"
    FOLLOW_UP = "follow_up"
    CONVERSATION_REFERENCE = "conversation_reference"
    GENERAL_QUESTION = "general_question"

class InteractionUnderstanding(HIOSModel):

    explicit_intents: list[str] = Field(
        default_factory=list,
    )
    interaction_type: InteractionType = (
        InteractionType.NEW_REQUEST
    )


class InteractionUnderstandingOutput(BaseModel):
    interaction_type: InteractionType
    explicit_intents: list[str] = Field(
        default_factory=list,
    )