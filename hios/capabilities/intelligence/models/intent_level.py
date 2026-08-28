from enum import Enum


class IntentLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"