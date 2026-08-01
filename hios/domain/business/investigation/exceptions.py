class InvestigationError(Exception):
    """
    Base investigation exception.
    """


class InvestigationAlreadyCompleted(
    InvestigationError
):
    pass


class InvestigationArchived(
    InvestigationError
):
    pass


class InvalidStatusTransition(
    InvestigationError
):
    pass


class MissingObservation(
    InvestigationError
):
    pass