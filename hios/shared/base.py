from pydantic import BaseModel, ConfigDict


class HIOSModel(BaseModel):
    """
    Base model for every HIOS domain object.

    Rules:
        - Immutable
        - Strict validation
        - No extra fields
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
    )