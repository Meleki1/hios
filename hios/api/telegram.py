from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
)

from hios.capabilities.assistant.telegram.models import (
    TelegramUpdate,
)
from hios.capabilities.assistant.telegram.webhook import (
    TelegramWebhookHandler,
)
from hios.api.dependencies import (
    get_telegram_webhook_handler,
)
from hios.core.config import get_settings


router = APIRouter(
    prefix="/webhooks",
    tags=["telegram"],
)


@router.post("/telegram")
async def telegram_webhook(
    update: TelegramUpdate,
    handler: TelegramWebhookHandler = Depends(
        get_telegram_webhook_handler,
    ),
    secret_token: str | None = Header(
        default=None,
        alias="X-Telegram-Bot-Api-Secret-Token",
    ),
) -> dict[str, bool]:

    settings = get_settings()

    if secret_token != settings.telegram_webhook_secret:
        raise HTTPException(
            status_code=403,
            detail="Invalid Telegram webhook secret",
        )

    await handler.handle(update)

    return {
        "ok": True,
    }