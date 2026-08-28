from hios.shared.base import HIOSModel
from hios.intelligence.conditions.condition import Condition


class Rule(HIOSModel):
    """
    A single declarative knowledge rule.
    """

    id: str

    name: str

    description: str | None = None

    condition: Condition

    facts: list[str]

    score: float = 1.0

    priority: int = 100
    
    enabled: bool = True

    tags: list[str] = []