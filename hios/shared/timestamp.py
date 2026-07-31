from datetime import datetime

from hios.shared.base import HIOSModel


class Timestamp(HIOSModel):

    created_at: datetime

    updated_at: datetime