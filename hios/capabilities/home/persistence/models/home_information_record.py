from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class HomeInformationRecord(Base):

    __tablename__ = "home_information"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    home_id: Mapped[str] = mapped_column(
        ForeignKey("homes.id"),
        nullable=False,
        index=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    postcode: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )