from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.reflection.models.reflection import Reflection


class Learner(
    ABC,
):

    @abstractmethod
    def learn(
        self,
        reflection: Reflection,
    ) -> Learning:

        raise NotImplementedError