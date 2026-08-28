from hios.shared.base import HIOSModel


class LocalActivityTrend(HIOSModel):

    category: str

    event_count: int

    intensity: float

    trend: str