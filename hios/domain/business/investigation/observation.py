from __future__ import annotations

from collections.abc import Iterator

from hios.domain.business.observation.models import Observation
from hios.shared.value_object import ValueObject


class Observations(ValueObject):
    """
    Immutable collection of observations.
    """

    items: tuple[Observation, ...] = ()

    def add(
        self,
        observation: Observation,
    ) -> "Observations":

        return self.model_copy(
            update={
                "items": (
                    *self.items,
                    observation,
                )
            }
        )

    def latest(self) -> Observation | None:

        if not self.items:
            return None

        return self.items[-1]

    def __len__(self):

        return len(self.items)

    def __iter__(
        self,
    ) -> Iterator[Observation]:

        return iter(self.items)