from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import Field

from hios.shared.value_object import ValueObject


class EntityId(ValueObject):
    """
    Globally unique identifier for Entities.
    """

    value: UUID = Field(default_factory=uuid4)

    @classmethod
    def new(cls) -> "EntityId":
        return cls(value=str(uuid4()))