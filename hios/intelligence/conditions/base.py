from __future__ import annotations

from abc import ABC

from hios.shared.base import HIOSModel


class Condition(
    HIOSModel,
    ABC,
):
    """
    Base class for every logical condition.
    """