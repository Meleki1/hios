from hios.capabilities.assistant.models.outreach_decision import (
    OutreachDecision,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.outreach.contracts import OutreachRequest
from hios.capabilities.outreach.models import OutreachChannel
from hios.capabilities.outreach.default_capability import DefaultOutreachCapability
from hios.runtime.context import RuntimeContext


class AssistantOutreachService:

    def __init__(
        self,
        *,
        outreach: DefaultOutreachCapability,
    ) -> None:
        self._outreach = outreach

    def decide(
        self,
        recommendation: MaintenanceRecommendation,
    ) -> OutreachDecision:

        if recommendation.priority == "high":
            return OutreachDecision(
                required=True,
                reason=(
                    "High-priority maintenance "
                    "requires user outreach."
                ),
            )

        return OutreachDecision(
            required=False,
            reason=(
                "Maintenance priority does not "
                "require immediate outreach."
            ),
        )

    async def send_maintenance_outreach(
        self,
        *,
        recommendation: MaintenanceRecommendation,
        recipient: str,
    ):
        decision = self.decide(recommendation)

        if not decision.required:
            return None

        request = OutreachRequest(
            recipient=recipient,
            subject=(
                f"HIOS Maintenance Alert: "
                f"{recommendation.task}"
            ),
            message=(
                "HIOS has identified a maintenance item "
                "that may require your attention.\n\n"
                f"Task: {recommendation.task}\n"
                f"Reason: {recommendation.reason}\n"
                f"Priority: {recommendation.priority}\n\n"
                "Please consider scheduling this maintenance."
            ),
            channel=OutreachChannel.EMAIL,
        )

        return await self._outreach.reason(
            request,
            RuntimeContext(),
        )