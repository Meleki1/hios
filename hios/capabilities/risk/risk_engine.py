from abc import ABC, abstractmethod

from hios.capabilities.risk.models.risk_score import RiskScore


class RiskEngine(ABC):

    @abstractmethod
    async def assess(
        self,
        risk_type: str,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
    ) -> RiskScore:
        raise NotImplementedError