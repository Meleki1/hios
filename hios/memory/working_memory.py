from __future__ import annotations

from typing import Any

from pydantic import Field

from hios.shared.base import HIOSModel


class WorkingMemory(HIOSModel):
    """
    Shared working memory for a single process execution.
    """

    values: dict[str, Any] = Field(default_factory=dict)

    def put(
        self,
        key: str,
        value: Any,
    ) -> None:
        self.values[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self.values.get(key, default)

    def contains(
        self,
        key: str,
    ) -> bool:
        return key in self.values

    def remove(
        self,
        key: str,
    ) -> None:
        self.values.pop(key, None)

    def clear(self) -> None:
        self.values.clear()

    def keys(self) -> list[str]:
        return list(self.values.keys())


    def items(self):
        return self.values.items()