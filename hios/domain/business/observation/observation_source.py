from enum import Enum

class ObservationSource(str, Enum):
    USER = "USER"
    CAMERA = "CAMERA"
    SENSOR = "SENSOR"
    SYSTEM = "SYSTEM"
