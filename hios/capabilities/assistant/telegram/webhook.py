from hios.capabilities.assistant.chat import (
    ChatRequest,
    HomeAssistantChat,
)

from hios.capabilities.assistant.telegram.client import (
    TelegramClient,
)

from hios.capabilities.assistant.telegram.models import (
    TelegramCallbackQuery,
    TelegramMessage,
    TelegramUpdate,
)
from hios.capabilities.assistant.telegram.provisioning import (
    TelegramProvisioningService,
)
from hios.capabilities.assistant.telegram.reply_markup import (
    inline_keyboard_from_reply_options,
    message_from_callback_data,
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
        if update.callback_query is not None:
            await self._handle_callback_query(
                update.callback_query,
            )
            return

        message = update.message

        if message is None:
            return

        await self._handle_message(message)

    async def _handle_callback_query(
        self,
        callback_query: TelegramCallbackQuery,
    ) -> None:
        text = message_from_callback_data(
            callback_query.data,
        )
        callback_message = callback_query.message

        if text is None or callback_message is None:
            await self._telegram.answer_callback_query(
                callback_query_id=callback_query.id,
            )
            return

        chat_id = callback_message.chat.id
        telegram_user_id = str(callback_query.from_.id)

        subject_id, home_id = (
            await self._provisioning_service.provision(
                telegram_user_id,
            )
        )

        result = await self._assistant.send(
            ChatRequest(
                subject_id=subject_id,
                home_id=home_id,
                message=text,
                conversation_id=str(chat_id),
            )
        )

        await self._telegram.answer_callback_query(
            callback_query_id=callback_query.id,
        )

        await self._telegram.send_message(
            chat_id=chat_id,
            text=result.message,
            reply_markup=inline_keyboard_from_reply_options(
                result.metadata.get("reply_options"),
            ),
        )

    async def _handle_message(
        self,
        message: TelegramMessage,
    ) -> None:
        has_photo = bool(message.photo)

        if not has_photo and message.text is None:
            return

        text = (message.text or message.caption or "").strip()

        if has_photo:
            text = text or "I've attached a photo of the issue."
        elif not text:
            return

        chat_id = message.chat.id

        telegram_user_id = str(message.from_.id)

        subject_id, home_id = (
            await self._provisioning_service.provision(
                telegram_user_id,
            )
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
                image=image,
            )
        )

        await self._telegram.send_message(
            chat_id=chat_id,
            text=result.message,
            reply_markup=inline_keyboard_from_reply_options(
                result.metadata.get("reply_options"),
            ),
        )
