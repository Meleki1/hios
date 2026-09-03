from __future__ import annotations
from enum import Enum
from hios.intelligence.evidence.model import Evidence
from hios.shared.base import HIOSModel

class HypothesisStatus(str, Enum):
    SUSPECTED = "suspected"
    CONFIRMED = "confirmed"

class Hypothesis(HIOSModel):
    """
    A possible explanation inferred from knowledge.
    """

    id: str

    name: str

    description: str

    confidence: float

    supporting_facts: list[str]

    evidence: list[Evidence]

    status: HypothesisStatus = HypothesisStatus.SUSPECTED