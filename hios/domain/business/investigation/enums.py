from enum import Enum


class InvestigationStatus(str, Enum):
    """
    Lifecycle of an investigation.
    """

    NEW = "NEW"

    ACTIVE = "ACTIVE"

    WAITING_FOR_INFORMATION = "WAITING_FOR_INFORMATION"

    READY_FOR_DECISION = "READY_FOR_DECISION"

    COMPLETED = "COMPLETED"

    ARCHIVED = "ARCHIVED"