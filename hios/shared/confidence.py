from hios.shared.base import HIOSModel
from hios.shared.enums import ConfidenceLevel


class Confidence(HIOSModel):

    level: ConfidenceLevel

    score: float