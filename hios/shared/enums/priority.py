from enum import Enum


class Priority(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    EMERGENCY = "EMERGENCY"


class ConfidenceLevel(str, Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class Severity(str, Enum):

    LOW = "LOW"

    MODERATE = "MODERATE"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


class ObservationType(str, Enum):

    TEXT = "TEXT"

    IMAGE = "IMAGE"

    VIDEO = "VIDEO"

    AUDIO = "AUDIO"

    DOCUMENT = "DOCUMENT"

    SENSOR = "SENSOR"


class SourceType(str, Enum):

    USER = "USER"

    SYSTEM = "SYSTEM"

    VISION = "VISION"

    SENSOR = "SENSOR"

    DOCUMENT = "DOCUMENT"