from typing import Any


def inline_keyboard_from_reply_options(
    reply_options: list[dict[str, str]] | None,
) -> dict[str, Any] | None:
    if not reply_options:
        return None

    buttons = []
    for option in reply_options:
        option_id = option.get("id")
        label = option.get("label")
        if not option_id or not label:
            continue
        buttons.append(
            {
                "text": label,
                "callback_data": option_id,
            }
        )

    if not buttons:
        return None

    return {
        "inline_keyboard": [buttons],
    }


def message_from_callback_data(
    callback_data: str | None,
) -> str | None:
    if not callback_data:
        return None
    return callback_data.strip() or None
