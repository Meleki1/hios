from dataclasses import dataclass


@dataclass(frozen=True)
class InvestigationQuestion:
    key: str
    question: str
    purpose: str