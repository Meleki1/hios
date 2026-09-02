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

        has_photo = bool(message.photo)

        if not has_photo and message.text is None:
            return

        text = (message.text or message.caption or "").strip()

        if has_photo:
            text = text or "I've attached a photo of the issue."
        elif not text:
            return

        chat_id = message.chat.id

        subject_id, home_id = (
            await self._provisioning_service.provision()
        )

        image = None

        if has_photo:
            largest_photo = message.photo[-1]

            image = await self._telegram.download_file(
                file_id=largest_photo.file_id,
            )


        result = await self._assistant.send(
            ChatRequest(
                subject_id=subject_id,
                home_id=home_id,
                message=text,
                conversation_id=str(chat_id),
                image = image,
            )
        )

        await self._telegram.send_message(
            chat_id=chat_id,
            text=result.message,
        )