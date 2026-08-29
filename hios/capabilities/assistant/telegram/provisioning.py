from uuid import uuid4

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
        *,
        subject_id: str | None = None,
        home_id: str | None = None,
    ) -> None:
        self._home_service = home_service
        self._home_repository = home_repository
        self._subject_id = subject_id
        self._home_id = home_id

    async def provision(self) -> tuple[str, str]:

        if self._subject_id and self._home_id:
            home = await self._home_repository.get(
                self._home_id,
            )

            if home is not None:
                return self._subject_id, home.id

        subject_id = self._subject_id or str(uuid4())

        home = await self._home_service.create(
            subject_id=subject_id,
            request=CreateHomeRequest(
                name="Telegram Test Home",
                home_type="residential",
                description=(
                    "Temporary home created for Telegram integration testing."
                ),
                information=HomeInformationInput(
                    country="Nigeria",
                    city="Lagos",
                    address="Telegram Test Address",
                    postcode=None,
                ),
            ),
        )

        return subject_id, home.id