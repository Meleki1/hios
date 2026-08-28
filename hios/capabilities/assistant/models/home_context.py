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
