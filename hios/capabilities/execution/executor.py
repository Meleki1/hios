from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.execution.models.execution import Execution


class Executor(
    ABC,
):

    @abstractmethod
    def execute(
        self,
        execution: Execution,
    ) -> Execution:

        raise NotImplementedError