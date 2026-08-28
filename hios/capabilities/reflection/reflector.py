from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.reflection.models.reflection import Reflection


class Reflector(
    ABC,
):

    @abstractmethod
    def reflect(
        self,
        outcome: Outcome,
    ) -> Reflection:

        raise NotImplementedError