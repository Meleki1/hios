from uuid import uuid4

from hios.capabilities.assistant.telegram.models import (
    TelegramIdentity,
)
from hios.capabilities.assistant.telegram.telegram_identity_repository import (
    TelegramIdentityRepository,
)
from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)
from hios.capabilities.home.services.home_service import HomeService
from hios.capabilities.home.repositories.home_repository import HomeRepository


class TelegramProvisioningService:

    def __init__(
        self,
        home_service: HomeService,
        home_repository: HomeRepository,
        identity_repository: TelegramIdentityRepository,
    ) -> None:
        self._home_service = home_service
        self._home_repository = home_repository
        self._identity_repository = identity_repository

    async def provision(
        self,
        telegram_user_id: str,
    ) -> tuple[str, str]:

        existing = (
            await self._identity_repository.get_by_telegram_user_id(
                telegram_user_id,
            )
        )

        if existing is not None:
            return existing.subject_id, existing.home_id

        subject_id = str(uuid4())

        home = await self._home_service.create(
            subject_id=subject_id,
            request=CreateHomeRequest(
                name="Telegram Home",
                home_type="residential",
                description=(
                    "Home created automatically from a Telegram "
                    "conversation."
                ),
                information=HomeInformationInput(
                    country="Nigeria",
                    city="Lagos",
                    address="Telegram Test Address",
                    postcode=None,
                ),
            ),
        )
        await self._identity_repository.save(
            TelegramIdentity(
                telegram_user_id=telegram_user_id,
                subject_id=subject_id,
                home_id=home.id,
            ),
        )

        return subject_id, home.id
