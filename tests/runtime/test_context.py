from hios.runtime.context import RuntimeContext


def test_context_has_execution_id():
    context = RuntimeContext()

    assert context.execution_id is not None


def test_context_has_started_at():
    context = RuntimeContext()

    assert context.started_at is not None


def test_context_metadata_defaults_empty():
    context = RuntimeContext()

    assert context.metadata == {}