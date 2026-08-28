from hios.shared.base import HIOSModel


class OutreachDecision(HIOSModel):
    required: bool = False
    reason: str = ""
    priority: str | None = None