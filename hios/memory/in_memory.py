from hios.memory.memory_record import MemoryRecord
from hios.memory.store import MemoryStore


class InMemoryMemoryStore(MemoryStore):

    def __init__(self):

        self._storage: dict[
            tuple[str, str],
            MemoryRecord,
        ] = {}

    def save(
        self,
        record: MemoryRecord,
    ) -> None:

        self._storage[
            (
                record.namespace,
                record.key,
            )
        ] = record

    def load(
        self,
        namespace: str,
        key: str,
    ) -> MemoryRecord | None:

        return self._storage.get(
            (
                namespace,
                key,
            )
        )

    def delete(
        self,
        namespace: str,
        key: str,
    ) -> None:

        self._storage.pop(
            (
                namespace,
                key,
            ),
            None,
        )

    def list(
        self,
        namespace: str,
    ) -> list[MemoryRecord]:

        return [
            record
            for (ns, _), record in self._storage.items()
            if ns == namespace
        ]