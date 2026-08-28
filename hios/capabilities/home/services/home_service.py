from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)

from hios.capabilities.home.repositories.home_repository import (
    HomeRepository,
)
from hios.capabilities.home.repositories.home_information_repository import (
    HomeInformationRepository,
)
from hios.capabilities.home.repositories.home_state_repository import (
    HomeStateRepository,
)

from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
)
from hios.capabilities.home.validators.home_creation import (
    HomeCreationValidator,
)
from hios.capabilities.home.events.home_created import (
    HomeCreatedEvent,
)


class HomeService:

    def __init__(
        self,
        home_repository: HomeRepository,
        information_repository: HomeInformationRepository,
        state_repository: HomeStateRepository,
        event_publisher=None,
    ):
        self._home_repository = home_repository
        self._information_repository = (
            information_repository
        )
        self._state_repository = (
            state_repository
        )
        self._event_publisher = event_publisher

    async def create(
        self,
        subject_id: str,
        request: CreateHomeRequest,
    ) -> Home:


        HomeCreationValidator.validate(
            name=request.name,
            home_type=request.home_type,
        )
        home = Home(
            name=request.name,
            home_type=request.home_type,
            description=request.description,
            status="active",
        )

        home = await self._home_repository.save(
            home,
        )

        information = HomeInformation(
            home_id=home.id,
            country=request.information.country,
            city=request.information.city,
            address=request.information.address,
            postcode=request.information.postcode,
        )

        await self._information_repository.save(
            information,
        )

        state = HomeState(
            home_id=home.id,
            status="active",
        )

        await self._state_repository.save(
            state,
        )

        if self._event_publisher is not None:

            await self._event_publisher.publish(
                HomeCreatedEvent(
                    home_id=home.id,
                    subject_id=subject_id,
                )
            )

        return home