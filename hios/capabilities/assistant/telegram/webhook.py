from hios.capabilities.assistant.chat import (
    ChatRequest,
    HomeAssistantChat,
)

from hios.capabilities.assistant.telegram.client import (
    TelegramClient,
)

from hios.capabilities.assistant.telegram.models import (
    TelegramUpdate,
)
from hios.capabilities.assistant.telegram.provisioning import (
    TelegramProvisioningService,
)


class TelegramWebhookHandler:

    def __init__(
        self,
        *,
        assistant: HomeAssistantChat,
        telegram: TelegramClient,
        provisioning_service: TelegramProvisioningService,
    ) -> None:
        self._assistant = assistant
        self._telegram = telegram
        self._provisioning_service = provisioning_service

    async def handle(
        self,
        update: TelegramUpdate,
    ) -> None:
        message = update.message

        if message is None:
            return

        if message.text is None:
            return

        text = message.text.strip()

        if not text:
            return

        chat_id = message.chat.id

        subject_id, home_id = (
            await self._provisioning_service.provision()
        )

        result = await self._assistant.send(
            ChatRequest(
                subject_id=subject_id,
                home_id=home_id,
                message=text,
                conversation_id=str(chat_id),
            )
        )

        await self._telegram.send_message(
            chat_id=chat_id,
            text=result.message,
        )