from dataclasses import dataclass, field

from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)
from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)


@dataclass
class IntelligenceContext:

    subject_id: str

    property_profile: PropertyProfile | None = None

    environmental_observation: (
        EnvironmentalObservation | None
    ) = None

    explicit_intents: list[str] = field(
        default_factory=list,
    )

    interactions: list[str] = field(
        default_factory=list,
    )

    local_activities: dict[str, str] = field(
        default_factory=dict,
    )

    platform_behaviours: dict[str, str] = field(
        default_factory=dict,
    )