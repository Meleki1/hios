from __future__ import annotations

from hios.shared.base import HIOSModel


class EvaluationResult(HIOSModel):

    matched: bool

    score: float

    matched_operands: list[str]

    unmatched_operands: list[str]

    duration_ms: float = 0.0