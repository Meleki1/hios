from abc import ABC, abstractmethod

from hios.capabilities.maintenance.models.maintenance_recommendation import MaintenanceRecommendation
from hios.capabilities.assistant.models.outreach_decision import OutreachDecision
from hios.capabilities.timeline.models.timeline_entry import TimelineEntry

class OutreachPolicy(ABC):

    @abstractmethod
    def decide(
        self,
        recommendation: MaintenanceRecommendation,
        timeline: list[TimelineEntry] | None = None,
    ) -> OutreachDecision:
        ...


class DefaultOutreachPolicy(OutreachPolicy):

    def decide(
        self,
        recommendation: MaintenanceRecommendation,
        timeline: list[TimelineEntry] | None = None,
    ) -> OutreachDecision:

        if recommendation.priority not in {"high", "critical"}:
            return OutreachDecision(
                required=False,
                reason=(
                    "The maintenance recommendation does not "
                    "currently require proactive outreach."
                ),
                priority=recommendation.priority,
            )

        timeline = timeline or []

        already_notified = any(
            entry.event_type == "outreach"
            and entry.event_name == "maintenance_alert_sent"
            and entry.resource_type == "maintenance"
            and entry.resource_id == recommendation.task
            for entry in timeline
        )

        if already_notified:
            return OutreachDecision(
                required=False,
                reason=(
                    "This maintenance recommendation has "
                    "already been communicated to the user."
                ),
                priority=recommendation.priority,
            )

        return OutreachDecision(
            required=True,
            reason=(
                "A high-priority maintenance recommendation "
                "requires user notification."
            ),
            priority=recommendation.priority,
        )