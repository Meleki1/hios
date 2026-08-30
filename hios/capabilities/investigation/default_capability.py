from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)
from hios.capabilities.memory.investigation.question_selector import (
    InvestigationQuestionSelector,
)
from hios.capabilities.memory.investigation.service import (
    InvestigationMemoryService,
)

from .contract import InvestigationCapability


class DefaultInvestigationCapability(
    InvestigationCapability,
):

    def __init__(
        self,
        selector: InvestigationQuestionSelector,
        memory: InvestigationMemoryService,
    ) -> None:
        self._selector = selector
        self._memory = memory

    async def next_question(
        self,
        *,
        investigation_id: str,
        hypothesis_name: str | None = None,
    ) -> InvestigationQuestion | None:

        question = await self._selector.select_next(
            investigation_id=investigation_id,
            hypothesis_name=hypothesis_name,
        )

        if question is None:
            return None

        await self._memory.remember_question(
            investigation_id=investigation_id,
            question_key=question.key,
            question=question.question,
        )

        return question

    async def remember_answer(
        self,
        *,
        investigation_id: str,
        question_key: str,
        answer: str,
    ) -> None:

        await self._memory.remember_answer(
            investigation_id=investigation_id,
            question_key=question_key,
            answer=answer,
        )