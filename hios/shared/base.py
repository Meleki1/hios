from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HIOSModel(BaseModel):
    """
    Root model for every object in HIOS.

    Responsibilities
    ----------------
    - Strict validation
    - Immutable by default
    - Consistent serialization
    - Shared configuration

    Notes
    -----
    Every Entity and ValueObject ultimately inherits from HIOSModel.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=False,
        arbitrary_types_allowed=False,
    )