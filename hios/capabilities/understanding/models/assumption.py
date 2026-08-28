from hios.shared.base import HIOSModel


class Assumption(HIOSModel):
    """
    An assumption made while interpreting knowledge.
    """

    description: str

    reason: str