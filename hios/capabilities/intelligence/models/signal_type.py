from enum import Enum


class SignalType(str, Enum):
    EXPLICIT_INTENT = "explicit_intent"
    CONVERSATION = "conversation"
    PROPERTY = "property"
    ENVIRONMENTAL = "environmental"
    LOCAL_ACTIVITY = "local_activity"
    PLATFORM_BEHAVIOUR = "platform_behaviour"
    IMAGE = "image"