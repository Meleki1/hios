from abc import ABC, abstractmethod
from collections.abc import Sequence

from .question import InvestigationQuestion


class InvestigationQuestionProvider(ABC):

    @abstractmethod
    def get_questions(
        self,
        *,
        hypothesis_name: str | None = None,
    ) -> Sequence[InvestigationQuestion]:
        ...