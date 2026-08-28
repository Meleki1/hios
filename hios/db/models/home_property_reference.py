from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from hios.db.base import Base


class HomePropertyReferenceRecord(Base):

    __tablename__ = "home_property_references"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    home_id: Mapped[str] = mapped_column(
        ForeignKey("homes.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    uprn: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )