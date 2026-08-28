from enum import Enum


class CapabilityType(str, Enum):
    KNOWLEDGE = "knowledge"
    UNDERSTANDING = "understanding"
    DECISION = "decision"
    EXECUTION = "execution"
    LEARNING = "learning"
    PEST_CONTROL = "pest_control"