from hios.capabilities.risk.models.risk_score import RiskScore
from hios.shared.base import HIOSModel


class RiskAssessment(HIOSModel):

    risks: list[RiskScore]