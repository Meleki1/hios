from enum import Enum


class SignalSource(str, Enum):
    HOME_ASSIST = "home_assist"
    WEATHER = "weather"
    PROPERTY = "property"
    LOCAL_ACTIVITY = "local_activity"
    PLATFORM = "platform"
    IMAGE = "image"