from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from hios.shared.entity import Entity
from .observation_medium import ObservationMedium
from .observation_source import ObservationSource


class Observation(Entity):
    """
    Represents a single observed fact about reality.

    Observations are immutable facts and form the
    foundation of every Investigation.
    """

    source: ObservationSource

    medium: ObservationMedium

    content: str

    observed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    @property
    def is_image(self) -> bool:
        return self.medium is ObservationMedium.IMAGE

    @property
    def is_text(self) -> bool:
        return self.medium is ObservationMedium.TEXT

    @property
    def is_sensor(self) -> bool:
        return self.source is ObservationSource.SENSOR

    @property
    def is_user(self) -> bool:
        return self.source is ObservationSource.USER