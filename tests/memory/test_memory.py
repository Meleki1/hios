from hios.memory.in_memory import InMemoryMemoryStore
from hios.memory.memory_record import MemoryRecord
from hios.memory.working_memory import WorkingMemory
from hios.runtime.context import RuntimeContext

def test_memory_record_creation():

    record = MemoryRecord(
        key="facts",
        value=["rodent"],
    )

    assert record.namespace == "default"
    assert record.key == "facts"
    assert record.value == ["rodent"]

def test_memory_record_custom_namespace():

    record = MemoryRecord(
        namespace="knowledge",
        key="facts",
        value=[],
    )

    assert record.namespace == "knowledge"

def test_memory_record_generates_timestamps():

    record = MemoryRecord(
        key="facts",
        value=[],
    )

    assert record.created_at is not None
    assert record.updated_at is not None

def test_save_record():

    store = InMemoryMemoryStore()

    record = MemoryRecord(
        key="facts",
        value=["rodent"],
    )

    store.save(record)

    loaded = store.load(
        "default",
        "facts",
    )

    assert loaded == record

def test_overwrite_record():

    store = InMemoryMemoryStore()

    store.save(
        MemoryRecord(
            key="facts",
            value=["A"],
        )
    )

    store.save(
        MemoryRecord(
            key="facts",
            value=["B"],
        )
    )

    loaded = store.load(
        "default",
        "facts",
    )

    assert loaded.value == ["B"]

def test_delete_record():

    store = InMemoryMemoryStore()

    store.save(
        MemoryRecord(
            key="facts",
            value=[],
        )
    )

    store.delete(
        "default",
        "facts",
    )

    assert store.load(
        "default",
        "facts",
    ) is None

def test_namespaces_are_isolated():

    store = InMemoryMemoryStore()

    store.save(
        MemoryRecord(
            namespace="knowledge",
            key="facts",
            value=["A"],
        )
    )

    store.save(
        MemoryRecord(
            namespace="understanding",
            key="facts",
            value=["B"],
        )
    )

    assert store.load(
        "knowledge",
        "facts",
    ).value == ["A"]

    assert store.load(
        "understanding",
        "facts",
    ).value == ["B"]

def test_list_namespace_records():

    store = InMemoryMemoryStore()

    store.save(
        MemoryRecord(
            namespace="knowledge",
            key="a",
            value=1,
        )
    )

    store.save(
        MemoryRecord(
            namespace="knowledge",
            key="b",
            value=2,
        )
    )

    records = store.list(
        "knowledge",
    )

    assert len(records) == 2

def test_put_and_get():

    memory = WorkingMemory()

    memory.put(
        "facts",
        ["rodent"],
    )

    assert memory.get("facts") == ["rodent"]

def test_missing_key_returns_default():

    memory = WorkingMemory()

    assert memory.get(
        "missing",
        [],
    ) == []

def test_contains():

    memory = WorkingMemory()

    memory.put(
        "facts",
        [],
    )

    assert memory.contains("facts")

def test_remove():

    memory = WorkingMemory()

    memory.put(
        "facts",
        [],
    )

    memory.remove("facts")

    assert not memory.contains("facts")

def test_clear():

    memory = WorkingMemory()

    memory.put("a", 1)
    memory.put("b", 2)

    memory.clear()

    assert not memory.contains("a")
    assert not memory.contains("b")

def test_runtime_context_has_working_memory():

    context = RuntimeContext()

    context.working_memory.put(
        "facts",
        ["rodent"],
    )

    assert context.working_memory.get(
        "facts",
    ) == ["rodent"]