from __future__ import annotations

from typing import Union

from hios.shared.base import HIOSModel

from .operator import ConditionOperator


class Condition(HIOSModel):
    """
    Recursive logical condition.
    """

    operator: ConditionOperator

    operands: list[
        Union[
            str,
            "Condition",
        ]
    ]