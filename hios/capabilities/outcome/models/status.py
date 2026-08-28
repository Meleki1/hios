from enum import StrEnum

class OutcomeStatus(StrEnum):

    SUCCESS = "success"

    PARTIAL = "partial"

    FAILED = "failed"

    UNKNOWN = "unknown"