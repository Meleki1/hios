from __future__ import annotations

from hios.capabilities.safety.contract.result import SafetyGuidanceResult


def append_safety_guidance_to_message(
    message: str,
    safety_guidance: SafetyGuidanceResult | None,
    *,
    communicated_guidance: list[str] | None = None,
) -> tuple[str, list[str]]:
    """
    Append the standard precautions block for items not yet sent.
    Returns the updated message and the list of bullets appended.
    """

    if safety_guidance is None or not safety_guidance.guidance:
        return message, []

    communicated = set(communicated_guidance or [])
    new_guidance = [
        guidance
        for guidance in safety_guidance.guidance
        if guidance not in communicated
    ]

    if not new_guidance:
        return message, []

    safety = "\n".join(
        f"- {guidance}"
        for guidance in new_guidance
    )
    suffix = f"Safety guidance:\n{safety}"

    if not message:
        return suffix, new_guidance

    return f"{message}\n\n{suffix}", new_guidance
