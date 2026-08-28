from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class HomeStateRecord(Base):

    __tablename__ = "home_state"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    home_id: Mapped[str] = mapped_column(
        ForeignKey("homes.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )