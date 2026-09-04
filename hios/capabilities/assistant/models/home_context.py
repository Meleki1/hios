from dataclasses import dataclass, field
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


@dataclass
class HomeContext:
    """
    NOTE (found during audit, deliberately left as a dataclass for
    now -- see below): `maintenance_records` used to default to
    `pydantic.Field(default_factory=list)`. Stdlib dataclasses don't
    understand pydantic's Field descriptor at all -- it isn't
    `dataclasses.field()` -- so any HomeContext built without an
    explicit maintenance_records argument (several test fixtures do
    exactly this: FakeContextAssembler in tests/assistant/
    test_nodes.py and test_workflow.py) got a raw pydantic FieldInfo
    object assigned to that attribute instead of a list. FieldInfo
    is truthy but not iterable, so `for record in
    self.maintenance_records` in __str__ below would raise
    `TypeError: 'FieldInfo' object is not iterable` the first time
    such a context was ever stringified (e.g. for the
    response-generation prompt). Fixed below by using the correct
    `dataclasses.field(default_factory=list)`.

    Separately: this class is written into LangGraph checkpoint
    state on every single turn (assemble_context runs
    unconditionally), but hios/runtime/persistence/
    checkpoint_types.py's ALLOWED_CHECKPOINT_TYPES can only list
    pydantic BaseModel subclasses or Enums (see that file's own test,
    test_allowed_checkpoint_types_are_models_or_enums) -- so as a
    dataclass, HomeContext can never be registered there, and every
    checkpoint write on every conversation turn will keep warning
    (and eventually fail under LANGGRAPH_STRICT_MSGPACK) about an
    unregistered type. The natural fix is converting this to a
    pydantic model like every other type nested inside it -- but
    several existing test fixtures currently construct it with
    placeholder values that aren't valid instances of its field
    types (bare dicts like `home={"id": home_id}`, or even
    `object()`), which strict pydantic validation would reject. That
    conversion needs those fixtures updated in the same change, and
    a full test run to confirm nothing else relies on this class
    accepting loosely-typed placeholders -- left as a follow-up
    rather than done blind here.
    """

    home: Home
    information: HomeInformation
    state: HomeState
    property_profile: PropertyProfile | None = None
    memories: list[MemoryEntry] | None = None
    timeline: list[TimelineEntry] | None = None
    maintenance_records: list[Maintenance] = field(
        default_factory=list
    )


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
 
