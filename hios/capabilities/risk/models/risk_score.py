from enum import Enum

from hios.shared.base import HIOSModel


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskScore(HIOSModel):
    risk_type: str
    score: float
    level: RiskLevel
    confidence: float = 1.0