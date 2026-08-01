from abc import abstractmethod

from hios.contracts.capability import Capability
from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult


class KnowledgeRequest(CapabilityRequest):

    observation: Observation


class KnowledgeResult(CapabilityResult):

    knowledge: KnowledgeContext


class KnowledgeCapability(
    Capability[
        KnowledgeRequest,
        KnowledgeResult,
    ]
):

    @abstractmethod
    async def execute(
        self,
        request: KnowledgeRequest,
    ) -> KnowledgeResult:
        ...