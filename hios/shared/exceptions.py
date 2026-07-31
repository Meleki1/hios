class HIOSError(Exception):
    """Base exception for HIOS."""


class DomainError(HIOSError):
    """Domain model violations."""


class ValidationError(HIOSError):
    """Validation failures."""


class WorkflowError(HIOSError):
    """Workflow execution errors."""


class PlanningError(HIOSError):
    """Planning failures."""