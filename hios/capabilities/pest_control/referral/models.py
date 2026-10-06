from enum import StrEnum

from pydantic import Field

from hios.shared.base import HIOSModel


class PestReferralPhase(StrEnum):
    INACTIVE = "inactive"
    AWAITING_CONSENT = "awaiting_consent"
    AWAITING_CONTACT_DETAILS = "awaiting_contact_details"
    AWAITING_SUBMIT_CONFIRMATION = "awaiting_submit_confirmation"
    SUBMITTED = "submitted"
    DECLINED = "declined"


class PestControlClientContact(HIOSModel):
    full_name: str | None = None
    address: str | None = None
    email: str | None = None
    phone: str | None = None


class PestControlReferralState(HIOSModel):
    phase: PestReferralPhase = PestReferralPhase.INACTIVE
    issue_id: str | None = None
    confirmed_problem: str = ""
    urgency: str = "medium"
    contact: PestControlClientContact = Field(
        default_factory=PestControlClientContact,
    )
    consent_granted: bool = False
    submission_reference: str | None = None


class PestControlContactSubmissionRequest(HIOSModel):
    contact_url: str
    full_name: str
    address: str
    email: str
    phone: str
    problem_description: str
    urgency: str


class PestControlContactSubmissionResult(HIOSModel):
    success: bool
    detail: str
