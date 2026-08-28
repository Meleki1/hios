from hios.capabilities.assistant.models.home_context import (
    HomeContext,
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
from hios.capabilities.property.service import PropertyService
from hios.capabilities.memory.service import MemoryService
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.home.services.home_property_service import (
    HomePropertyService,
)
from hios.capabilities.maintenance.repositories.maintenance_repository import (
    MaintenanceRepository,
)


class HomeContextAssembler:

    def __init__(
        self,
        home_repository: HomeRepository,
        information_repository: HomeInformationRepository,
        state_repository: HomeStateRepository,
        maintenance_repository: MaintenanceRepository | None = None,
        property_service: PropertyService | None = None,
        memory_service: MemoryService | None = None,
        timeline_service: TimelineService | None = None,
        home_property_service: HomePropertyService | None = None,
    ):
        self._home_repository = home_repository
        self._information_repository = (
            information_repository
        )
        self._state_repository = state_repository
        self._maintenance_repository = (
            maintenance_repository
        )
        self._property_service = property_service
        self._memory_service = memory_service
        self._timeline_service = timeline_service
        self._home_property_service = (
            home_property_service
        )

    async def assemble(
        self,
        home_id: str,
        subject_id: str,
        message: str | None = None,
    ) -> HomeContext:

        home = await self._home_repository.get(
            home_id,
        )

        if home is None:
            raise ValueError(
                "Home not found"
            )

        information = await (
            self._information_repository.get_by_home(
                home_id,
            )
        )

        if information is None:
            raise ValueError(
                "Home information not found"
            )

        state = await (
            self._state_repository.get_by_home(
                home_id,
            )
        )

        if state is None:
            raise ValueError(
                "Home state not found"
            )

        maintenance_records = []

        if self._maintenance_repository is not None:
            maintenance_records = (
                await self._maintenance_repository.get_by_home(
                    home_id
                )
            )

        property_profile = None

        if (
            self._home_property_service is not None
            and self._property_service is not None
        ):
            reference = await (
                self._home_property_service.get_by_home(
                    home_id,
                )
            )

            if reference is not None:
                property_profile = (
                    await self._property_service.get_property(
                        reference.uprn,
                    )
                )

        memories = []


        if (
            self._memory_service is not None
            and message
        ):
            memories = await self._memory_service.recall(
                query=message,
            )

        timeline = []

        if self._timeline_service is not None:
            timeline = await (
                self._timeline_service.get_by_subject(
                    subject_id,
                )
            )

        

        return HomeContext(
            home=home,
            information=information,
            state=state,
            property_profile=property_profile,
            memories=memories,
            timeline=timeline,
            maintenance_records=maintenance_records,
        )