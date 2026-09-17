from datetime import datetime, timezone

from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher
from hios.capabilities.outreach.contracts import OutreachRequest
from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)
from hios.runtime.context import RuntimeContext


class PredictionFeedbackService:
    """
    The first link in the product docs' own feedback loop diagram:

        Prediction -> Business contacted customer? -> Customer
        booked? -> Service completed? -> Satisfied? -> Model updated

    Everything downstream of "contacted customer" already exists and
    has zero callers today (OutcomeService.record, IntelligenceService
    .evaluate / PredictionEvaluationService -- see the
    intelligence-pipeline-wiring-audit project doc, gap 6). What was
    genuinely missing was any trigger that notices a prediction's
    horizon_days window has elapsed and asks the question at all.
    This service is that trigger's business logic:
    `send_due_checkins()` finds predictions with no recorded Outcome
    whose horizon has passed (PredictionRepository
    .list_due_for_feedback) and emails each household asking whether
    it panned out.

    Deliberately NOT done here: automatically recording the Outcome.
    There is no reply-capture mechanism anywhere in this codebase
    (no webhook, no reply-parsing, no "yes/no" link handler) that
    could turn a homeowner's response back into a structured
    `occurred: bool` -- inventing one blind wasn't something to guess
    at. Recording the outcome once the answer comes back (however it
    comes back) is a call to the already-built `OutcomeService
    .record()`; wiring that up is a separate, smaller follow-up once
    there's an actual answer-capture path to call it from.

    Two things this needs to run for real, neither of which exists
    in the codebase yet (flagged rather than guessed at -- see the
    project doc):

    - A schedule to actually call `send_due_checkins()` periodically.
      The product docs mention Airflow/Prefect as the intended stack;
      nothing under hios/api/ invokes this (or any) scheduled job
      today.
    - A way to resolve `subject_id -> email address` outside of a
      live conversation turn. Today the only place an email address
      exists anywhere is `metadata.email` on a single
      HomeAssistantRequest -- there is no Household/Contact
      repository that persists one. `recipient_resolver` is accepted
      as an injected async callable for exactly this reason, so this
      service can be built and tested now without fabricating that
      storage layer.
    """

    def __init__(
        self,
        *,
        prediction_repository,
        outreach,
        recipient_resolver,
        event_publisher: EventPublisher | None = None,
    ):
        self._prediction_repository = prediction_repository
        self._outreach = outreach
        self._recipient_resolver = recipient_resolver
        self._event_publisher = event_publisher

    async def send_due_checkins(
        self,
        as_of: datetime | None = None,
    ) -> dict:

        as_of = as_of or datetime.now(timezone.utc)

        due = (
            await self._prediction_repository.list_due_for_feedback(
                as_of=as_of,
            )
        )

        checked_in = []
        skipped_no_recipient = []
        skipped_delivery_failed = []

        for prediction in due:

            recipient = await self._recipient_resolver(
                prediction.subject_id,
            )

            if not recipient:
                skipped_no_recipient.append(prediction.id)
                continue

            result = await self._send_checkin(
                prediction=prediction,
                recipient=recipient,
            )

            if result.status == OutreachDeliveryStatus.SENT:
                checked_in.append(prediction.id)

                if self._event_publisher is not None:
                    await self._event_publisher.publish(
                        BaseEvent(
                            event_type="prediction_feedback",
                            event_name="checkin_sent",
                            state="sent",
                            description=(
                                "Feedback check-in sent for "
                                f"prediction {prediction.id}"
                            ),
                            subject_id=prediction.subject_id,
                            resource_id=prediction.id,
                            resource_type="prediction",
                        )
                    )
            else:
                skipped_delivery_failed.append(
                    prediction.id,
                )

        return {
            "checked_in": checked_in,
            "skipped_no_recipient": skipped_no_recipient,
            "skipped_delivery_failed": (
                skipped_delivery_failed
            ),
        }

    async def _send_checkin(
        self,
        *,
        prediction,
        recipient: str,
    ):

        target_label = prediction.target.replace(
            "_",
            " ",
        )

        return await self._outreach.reason(
            OutreachRequest(
                recipient=recipient,
                subject=(
                    "HIOS Check-in: did this end up helping?"
                ),
                message=(
                    "A little while ago we flagged a possible "
                    f"need for {target_label}.\n\n"
                    "Did you end up needing this, or has it "
                    "resolved itself? Letting us know helps us "
                    "give better advice in future."
                ),
                channel=OutreachChannel.EMAIL,
            ),
            RuntimeContext(),
        )
