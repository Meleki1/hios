from .question import InvestigationQuestion
from .service import InvestigationMemoryService
from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)
from hios.capabilities.memory.investigation.question_provider import (
    InvestigationQuestionProvider,
)



class InvestigationQuestionSelector:

    def __init__(
        self,
        memory: InvestigationMemoryService,
        provider: InvestigationQuestionProvider,
    ) -> None:
        self._memory = memory
        self._provider = provider

    async def select_next(
        self,
        *,
        investigation_id: str,
        hypothesis_name: str | None = None,
    ) -> InvestigationQuestion | None:

        questions = self._provider.get_questions(
            hypothesis_name=hypothesis_name,
        )

        for question in questions:
            if not await self._memory.has_asked(
                investigation_id=investigation_id,
                question_key=question.key,
            ):
                return question

        return None