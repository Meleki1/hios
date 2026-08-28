from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.outcome.models.outcome import Outcome


class OutcomeEvaluator(
    ABC,
):

    @abstractmethod
    def evaluate(
        self,
        execution: Execution,
    ) -> Outcome:

        raise NotImplementedError