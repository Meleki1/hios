from __future__ import annotations
import webbrowser
from dataclasses import dataclass

from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.consent.consent_workflow import ConsentWorkflow
from hios.capabilities.consent.models.consent import ConsentPurpose
from hios.capabilities.pest_control.models.assessment import PestAssessment
from hios.capabilities.pest_control.referral.contact_form_submitter import (
    PestControlContactFormSubmitter,
)
from hios.capabilities.pest_control.referral.message_parsing import (
    extract_address,
    extract_email,
    extract_name,
    extract_phone,
    is_affirmative,
    is_negative,
    is_submit_confirmation,
)
from hios.capabilities.pest_control.referral.models import (
    PestControlClientContact,
    PestControlContactSubmissionRequest,
    PestControlReferralState,
    PestReferralPhase,
)
from hios.capabilities.risk.models.risk_score import RiskLevel


@dataclass
class PestControlReferralTurnResult:
    referral: PestControlReferralState
    assistant_message: str | None = None
    replace_assistant_response: bool = False


class PestControlReferralHandler:

    def __init__(
        self,
        *,
        contact_url: str,
        contact_form_submitter: PestControlContactFormSubmitter,
        consent_workflow: ConsentWorkflow | None = None,
    ) -> None:
        self._contact_url = contact_url
        self._submitter = contact_form_submitter
        self._consent_workflow = consent_workflow

    async def advance(
        self,
        *,
        state: HomeAssistantState,
    ) -> PestControlReferralTurnResult:
        referral = _current_referral(state)
        assessment = state.get("assessment")

        if referral.phase in {
            PestReferralPhase.SUBMITTED,
            PestReferralPhase.DECLINED,
        }:
            return PestControlReferralTurnResult(
                referral=referral,
            )

        if referral.phase == PestReferralPhase.INACTIVE:
            if not _issue_is_confirmed(assessment):
                return PestControlReferralTurnResult(
                    referral=referral,
                )
            referral = _start_referral(
                referral,
                assessment=assessment,
                state=state,
            )
            return PestControlReferralTurnResult(
                referral=referral,
                assistant_message=_consent_prompt(referral),
                replace_assistant_response=False,
            )

        message = state.get("message", "")

        if referral.phase == PestReferralPhase.AWAITING_CONSENT:
            return await self._handle_consent(
                referral=referral,
                message=message,
                state=state,
            )

        if referral.phase == PestReferralPhase.AWAITING_CONTACT_DETAILS:
            return self._handle_contact_details(
                referral=referral,
                message=message,
            )

        if referral.phase == PestReferralPhase.AWAITING_SUBMIT_CONFIRMATION:
            return await self._handle_submit_confirmation(
                referral=referral,
                message=message,
                state=state,
            )

        return PestControlReferralTurnResult(
            referral=referral,
        )

    async def _handle_consent(
        self,
        *,
        referral: PestControlReferralState,
        message: str,
        state: HomeAssistantState,
    ) -> PestControlReferralTurnResult:
        if is_negative(message):
            referral = referral.model_copy(
                update={"phase": PestReferralPhase.DECLINED},
            )
            return PestControlReferralTurnResult(
                referral=referral,
                assistant_message=(
                    "Understood — I won't share your details with a "
                    "pest control partner. If you change your mind, "
                    "tell me and we can try again."
                ),
                replace_assistant_response=True,
            )

        if not is_affirmative(message):
            return PestControlReferralTurnResult(
                referral=referral,
                assistant_message=(
                    "Before I contact a pest control partner on your "
                    "behalf, I need your consent to share your name, "
                    "address, email, and phone, plus the problem we "
                    "confirmed and how urgent it is.\n\n"
                    "Reply yes to agree, or no to decline."
                ),
                replace_assistant_response=True,
            )

        contact = _prefill_contact_from_home(
            referral.contact,
            state=state,
        )
        referral = referral.model_copy(
            update={
                "consent_granted": True,
                "phase": PestReferralPhase.AWAITING_CONTACT_DETAILS,
                "contact": contact,
            },
        )

        return PestControlReferralTurnResult(
            referral=referral,
            assistant_message=_contact_details_prompt(referral),
            replace_assistant_response=True,
        )

    def _handle_contact_details(
        self,
        *,
        referral: PestControlReferralState,
        message: str,
    ) -> PestControlReferralTurnResult:
        contact = referral.contact
        contact_updates: dict[str, str] = {}

        name = extract_name(message)
        if name:
            contact_updates["full_name"] = name

        email = extract_email(message)
        if email:
            contact_updates["email"] = email

        phone = extract_phone(message)
        if phone:
            contact_updates["phone"] = phone

        address = extract_address(message)
        if address:
            contact_updates["address"] = address
        elif _looks_like_address_update(message, contact):
            contact_updates["address"] = message.strip()

        if contact_updates:
            contact = contact.model_copy(update=contact_updates)

        referral = referral.model_copy(update={"contact": contact})

        missing = _missing_contact_fields(contact)
        if missing:
            return PestControlReferralTurnResult(
                referral=referral,
                assistant_message=(
                    "Thanks — I still need: "
                    + ", ".join(missing)
                    + ".\n\n"
                    + _contact_details_prompt(referral)
                ),
                replace_assistant_response=True,
            )

        referral = referral.model_copy(
            update={
                "phase": PestReferralPhase.AWAITING_SUBMIT_CONFIRMATION,
            },
        )
        return PestControlReferralTurnResult(
            referral=referral,
            assistant_message=_submit_confirmation_prompt(referral),
            replace_assistant_response=True,
        )

    async def _handle_submit_confirmation(
        self,
        *,
        referral: PestControlReferralState,
        message: str,
        state: HomeAssistantState,
    ) -> PestControlReferralTurnResult:
        if not is_submit_confirmation(message):
            return PestControlReferralTurnResult(
                referral=referral,
                assistant_message=(
                    "Please review the summary below. To send this to "
                    "the pest control partner, reply exactly: "
                    "CONFIRM SUBMIT\n\n"
                    + _submit_confirmation_prompt(referral)
                ),
                replace_assistant_response=True,
            )

        if self._consent_workflow is not None:
            await self._consent_workflow.grant(
                subject_id=state["subject_id"],
                purpose=ConsentPurpose.BUSINESS_SHARING,
            )

        contact = referral.contact
        assert contact.full_name
        assert contact.address
        assert contact.email
        assert contact.phone

        submission = await self._submitter.submit(
            PestControlContactSubmissionRequest(
                contact_url=self._contact_url,
                full_name=contact.full_name,
                address=contact.address,
                email=contact.email,
                phone=contact.phone,
                problem_description=referral.confirmed_problem,
                urgency=referral.urgency,
            ),
        )

        referral = referral.model_copy(
            update={
                "phase": PestReferralPhase.SUBMITTED,
                "submission_reference": submission.detail,
            },
        )

        if submission.success:
            assistant_message = (
                "Done — I've submitted your contact request to the "
                "pest control partner with the confirmed problem and "
                "urgency. They should follow up with you directly."
            )
        else:
            assistant_message = (
                "I couldn't complete the website submission: "
                f"{submission.detail}. "
                "Your details were not sent. You can try again later "
                "or contact the provider directly through the attached link."
            )

        return PestControlReferralTurnResult(
            referral=referral,
            assistant_message=assistant_message,
            replace_assistant_response=True,
        )


def _current_referral(
    state: HomeAssistantState,
) -> PestControlReferralState:
    existing = state.get("pest_referral")
    if existing is not None:
        return existing
    return PestControlReferralState()


def _issue_is_confirmed(
    assessment: PestAssessment | None,
) -> bool:
    return assessment is not None and bool(
        assessment.pest_type or assessment.explanation,
    )


def _start_referral(
    referral: PestControlReferralState,
    *,
    assessment: PestAssessment,
    state: HomeAssistantState,
) -> PestControlReferralState:
    problem = assessment.explanation or assessment.pest_type or ""
    if assessment.pest_type and assessment.pest_type not in problem:
        problem = f"{assessment.pest_type}: {problem}".strip()

    return referral.model_copy(
        update={
            "issue_id": assessment.id,
            "confirmed_problem": problem.strip(),
            "urgency": _derive_urgency(state, assessment),
            "phase": PestReferralPhase.AWAITING_CONSENT,
        },
    )


def _derive_urgency(
    state: HomeAssistantState,
    assessment: PestAssessment,
) -> str:
    if assessment.severity:
        return assessment.severity

    risk = state.get("risk")
    if risk is not None and risk.risks:
        levels = [entry.level for entry in risk.risks]
        if RiskLevel.HIGH in levels:
            return "high"
        if RiskLevel.MEDIUM in levels:
            return "medium"
    return "medium"


def _prefill_contact_from_home(
    contact: PestControlClientContact,
    *,
    state: HomeAssistantState,
) -> PestControlClientContact:
    context = state.get("context")
    if context is None:
        return contact

    information = context.information
    address_parts = [
        part
        for part in (
            information.address,
            information.city,
            information.postcode,
            information.country,
        )
        if part
    ]
    if address_parts:
        return contact.model_copy(
            update={"address": ", ".join(address_parts)},
        )
    return contact


def _missing_contact_fields(
    contact: PestControlClientContact,
) -> list[str]:
    missing: list[str] = []
    if not contact.full_name:
        missing.append("full name")
    if not contact.address:
        missing.append("service address")
    if not contact.email:
        missing.append("email address")
    if not contact.phone:
        missing.append("phone number")
    return missing


def _consent_prompt(
    referral: PestControlReferralState,
) -> str:
    return (
        "We've confirmed the issue"
        + (
            f" ({referral.confirmed_problem})"
            if referral.confirmed_problem
            else ""
        )
        + ". I can reach out to a pest control partner through "
        "their contact form with your details, the confirmed "
        f"problem, and urgency ({referral.urgency}).\n\n"
        "Do you consent to me sharing your name, address, email, "
        "and phone for that purpose? Reply yes or no."
    )


def _contact_details_prompt(
    referral: PestControlReferralState,
) -> str:
    contact = referral.contact
    lines = [
        "Please send your full name, email, and phone number.",
    ]
    if contact.address:
        lines.append(
            f"I have this address on file: {contact.address}. "
            "Reply with a corrected address if needed."
        )
    else:
        lines.append("Include your service address as well.")
    return "\n".join(lines)


def _submit_confirmation_prompt(
    referral: PestControlReferralState,
) -> str:
    contact = referral.contact
    return (
        "Please confirm this summary before I submit it to the "
        "pest control partner:\n"
        f"Name: {contact.full_name}\n"
        f"Address: {contact.address}\n"
        f"Email: {contact.email}\n"
        f"Phone: {contact.phone}\n"
        f"Problem: {referral.confirmed_problem}\n"
        f"Urgency: {referral.urgency}\n\n"
        "Reply CONFIRM SUBMIT to send, or tell me what to change."
    )


def _looks_like_address_update(
    message: str,
    contact: PestControlClientContact,
) -> bool:
    lowered = message.lower()
    if extract_email(message) or extract_phone(message):
        return False
    if contact.address and contact.address.lower() in lowered:
        return True
    street_markers = (
        "street",
        "st ",
        " road",
        " rd",
        " avenue",
        " ave",
        " lane",
        " drive",
        " dr",
    )
    return any(marker in lowered for marker in street_markers)
