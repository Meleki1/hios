from enum import Enum


class AssistantDomain(str, Enum):

    CONVERSATION = "conversation"

    HOME = "home"

    PEST_CONTROL = "pest_control"

    UNSUPPORTED = "unsupported"