from abc import ABC, abstractmethod

from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)


class InvestigationCapability(ABC):

    @abstractmethod
    async def next_question(
        self,
        *,
        investigation_id: str,
        hypothesis_name: str | None = None,
    ) -> InvestigationQuestion | None:
        ...

    @abstractmethod
    async def remember_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
        answer: str,
    ) -> None:
        ...