from uuid import uuid4
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.memory.store import MemoryStore

from .models import InvestigationMemoryCategory


class InvestigationMemoryService:

    def __init__(
        self,
        store: MemoryStore,
    ) -> None:
        self._store = store

    async def remember_question(
        self,
        *,
        investigation_id: str,
        question_key: str,
        question: str,
    ) -> MemoryEntry:
        raise NotImplementedError

    async def has_asked(
        self,
        *,
        investigation_id: str,
        question_key: str,
    ) -> bool:
        raise NotImplementedError

    async def remember_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
        answer: str,
    ) -> MemoryEntry:
        raise NotImplementedError

    async def get_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
    ) -> str | None:
        raise NotImplementedError




class InvestigationMemoryService:

    def __init__(
        self,
        store: MemoryStore,
    ) -> None:
        self._store = store

    async def remember_question(
        self,
        *,
        investigation_id: str,
        question_key: str,
        question: str,
    ) -> MemoryEntry:

        memory = MemoryEntry(
            id=str(uuid4()),
            category=InvestigationMemoryCategory.QUESTION,
            description=question,
            confidence=1.0,
            details={
                "investigation_id": investigation_id,
                "question_key": question_key,
                "status": "asked",
            },
        )

        await self._store.store([memory])

        return memory

    async def has_asked(
        self,
        *,
        investigation_id: str,
        question_key: str,
    ) -> bool:

        memories = await self._store.retrieve(
            query=question_key,
            category=InvestigationMemoryCategory.QUESTION,
        )

        return any(
            memory.details.get("investigation_id")
            == investigation_id
            and memory.details.get("question_key")
            == question_key
            for memory in memories
        )

    async def remember_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
        answer: str,
    ) -> MemoryEntry:

        memory = MemoryEntry(
            id=str(uuid4()),
            category=InvestigationMemoryCategory.ANSWER,
            description=answer,
            confidence=1.0,
            details={
                "investigation_id": investigation_id,
                "question_key": question_key,
                "status": "answered",
            },
        )

        await self._store.store([memory])

        return memory

    async def get_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
    ) -> str | None:

        memories = await self._store.retrieve(
            query=question_key,
            category=InvestigationMemoryCategory.ANSWER,
        )

        for memory in memories:
            if (
                memory.details.get("investigation_id")
                == investigation_id
                and memory.details.get("question_key")
                == question_key
                and memory.details.get("status")
                == "answered"
            ):
                return memory.description

        return None

    