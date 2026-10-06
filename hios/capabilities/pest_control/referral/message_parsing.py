import re

_AFFIRMATIVE = {
    "yes",
    "y",
    "yeah",
    "yep",
    "sure",
    "ok",
    "okay",
    "agree",
    "i agree",
    "please do",
    "go ahead",
    "sounds good",
}

_NEGATIVE = {
    "no",
    "n",
    "nope",
    "don't",
    "do not",
    "not now",
    "decline",
    "cancel",
}

_SUBMIT_CONFIRM = {
    "confirm submit",
    "yes submit",
    "submit",
    "send it",
    "go ahead and submit",
    "i confirm",
    "confirmed",
}

_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
)

_PHONE = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}",
)


def _normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def is_affirmative(message: str) -> bool:
    normalized = _normalize(message)
    if normalized in _AFFIRMATIVE:
        return True
    return any(
        phrase in normalized
        for phrase in (
            "yes",
            "i agree",
            "go ahead",
            "please do",
        )
    )


def is_negative(message: str) -> bool:
    normalized = _normalize(message)
    if normalized in _NEGATIVE:
        return True
    return normalized.startswith("no ") or normalized == "no"


def is_submit_confirmation(message: str) -> bool:
    normalized = _normalize(message)
    if normalized in _SUBMIT_CONFIRM:
        return True
    return "confirm" in normalized and "submit" in normalized


def extract_email(message: str) -> str | None:
    match = _EMAIL.search(message)
    if match is None:
        return None
    return match.group(0)


def extract_phone(message: str) -> str | None:
    match = _PHONE.search(message)
    if match is None:
        return None
    return match.group(0).strip()


def extract_address(message: str) -> str | None:
    normalized = _normalize(message)
    for prefix in (
        "address:",
        "address is ",
        "service address:",
        "service address is ",
    ):
        if prefix in normalized:
            start = normalized.index(prefix) + len(prefix)
            fragment = message[start:].strip()
            if fragment:
                return fragment.split("\n", maxsplit=1)[0].strip()
    return None


def extract_name(message: str) -> str | None:
    normalized = _normalize(message)
    for prefix in (
        "my name is ",
        "name is ",
        "i am ",
        "i'm ",
    ):
        if normalized.startswith(prefix):
            value = message.strip()[len(prefix) :].strip()
            for stop in (".", ",", " email", " phone"):
                if stop in value.lower():
                    value = value.split(stop, maxsplit=1)[0].strip()
            return value or None
    if "@" not in message and not _PHONE.search(message):
        stripped = message.strip()
        if 2 <= len(stripped.split()) <= 5:
            return stripped
    return None
