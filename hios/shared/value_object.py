from __future__ import annotations

from hios.shared.base import HIOSModel


class ValueObject(HIOSModel):
    """
    Base class for immutable domain value objects.

    Characteristics
    ---------------
    - Immutable
    - Compared by value
    - No identity
    - No lifecycle
    """

    __slots__ = ()