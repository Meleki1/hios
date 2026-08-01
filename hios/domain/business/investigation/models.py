from __future__ import annotations

from pydantic import Field

from hios.shared.aggregate_root import AggregateRoot

from .blocker import InvestigationBlocker
from .enums import InvestigationStatus
from .exceptions import (
    InvestigationAlreadyCompleted,
    InvestigationArchived,
    MissingObservation,
)
from hios.domain.business.investigation.observation import Observations
from hios.domain.business.observation.models import Observation


class Investigation(AggregateRoot):
    """
    Active reasoning process around a specific problem.
    """

    status: InvestigationStatus

    observations: Observations = Field(
        default_factory=Observations
    )

    blocker: InvestigationBlocker | None = None

    @classmethod
    def start(cls) -> "Investigation":
        return cls(
            status=InvestigationStatus.NEW
        )

    def record_observation(
        self,
        observation: Observation,
    ) -> "Investigation":

        if self.status == InvestigationStatus.ARCHIVED:
            raise InvestigationArchived()

        updated = self.observations.add(observation)

        return self.model_copy(
            update={
                "observations": updated,
                "status": InvestigationStatus.ACTIVE,
                "blocker": None,
            }
        )

    def request_information(
        self,
        reason: str,
    ) -> "Investigation":

        if self.status == InvestigationStatus.ARCHIVED:
            raise InvestigationArchived()

        if self.status == InvestigationStatus.COMPLETED:
            raise InvestigationAlreadyCompleted()

        return self.model_copy(
            update={
                "status": InvestigationStatus.WAITING_FOR_INFORMATION,
                "blocker": InvestigationBlocker(
                    reason=reason
                ),
            }
        )

    def complete(self) -> "Investigation":

        if self.status == InvestigationStatus.ARCHIVED:
            raise InvestigationArchived()

        if len(self.observations) == 0:
            raise MissingObservation()

        return self.model_copy(
            update={
                "status": InvestigationStatus.COMPLETED,
                "blocker": None,
            }
        )

    def archive(self) -> "Investigation":

        return self.model_copy(
            update={
                "status": InvestigationStatus.ARCHIVED
            }
        )