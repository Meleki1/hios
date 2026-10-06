from abc import ABC, abstractmethod

from hios.capabilities.assistant.telegram.models import (
    TelegramIdentity,
)


class TelegramIdentityRepository(ABC):

    @abstractmethod
    async def get_by_telegram_user_id(
        self,
        telegram_user_id: str,
    ) -> TelegramIdentity | None:
        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        identity: TelegramIdentity,
    ) -> TelegramIdentity:
        raise NotImplementedError
