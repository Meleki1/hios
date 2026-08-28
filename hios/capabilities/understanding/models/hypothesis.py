from __future__ import annotations

from hios.intelligence.evidence.model import Evidence
from hios.shared.base import HIOSModel


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