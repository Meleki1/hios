from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)
from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)
from hios.capabilities.memory.models.memory_entry import (
    MemoryEntry,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
)
from pydantic import Field

class HomeContext:

    def __init__(
        self,
        home: Home,
        information: HomeInformation,
        state: HomeState,
        property_profile: PropertyProfile | None = None,
        memories: list[MemoryEntry] | None = None,
        timeline: list[TimelineEntry] | None = None,
        maintenance_records: list[Maintenance] = Field(
            default_factory=list,
        )
    ):
        self.home = home
        self.information = information
        self.state = state
        self.property_profile = property_profile
        self.memories = memories or []
        self.timeline = timeline or []
        self.maintenance_records = maintenance_records

    def __str__(self) -> str:

        lines = [
            f"Home: {self.home}",
            f"Home information: {self.information}",
            f"Home state: {self.state}",
        ]

        lines.append(
            f"Property profile: {self.property_profile}"
            if self.property_profile is not None
           else "Property profile: none on file"
        )

        if self.memories:
            memory_lines = "\n".join(
                f"  - {memory.description}"
                for memory in self.memories
            )
            lines.append(f"Known memories:\n{memory_lines}")
        else:
            lines.append("Known memories: none")

        if self.maintenance_records:
            maintenance_lines = "\n".join(
                f"  - {record.task} ({record.status})"
                for record in self.maintenance_records
            )
            lines.append(
                f"Maintenance records:\n{maintenance_lines}"
            )
        else:
            lines.append("Maintenance records: none")

        return "\n".join(lines)
 
