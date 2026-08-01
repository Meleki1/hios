from enum import Enum




class ObservationMedium(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    STRUCTURED = "STRUCTURED"