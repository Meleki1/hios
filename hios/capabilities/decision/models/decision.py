from hios.shared.base import HIOSModel

from hios.capabilities.planning.models.plan import Plan


class Decision(HIOSModel):
    

    plan: Plan

    rationale: str

    score: float