import asyncio

from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)
from hios.capabilities.home.services.home_service import (
    HomeService,
)
from hios.capabilities.home.repositories.postgres_home_repository import (
    PostgresHomeRepository,
)
from hios.capabilities.home.repositories.postgres_home_information_repository import (
    PostgresHomeInformationRepository,
)
from hios.capabilities.home.repositories.postgres_home_state_repository import (
    PostgresHomeStateRepository,
)
from hios.db.session import SessionLocal


SUBJECT_ID = "telegram-test-subject"


async def main() -> None:
    async with SessionLocal() as session:
        home_repository = PostgresHomeRepository(
            session=session,
        )

        information_repository = (
            PostgresHomeInformationRepository(
                session=session,
            )
        )

        state_repository = PostgresHomeStateRepository(
            session=session,
        )

        service = HomeService(
            home_repository=home_repository,
            information_repository=information_repository,
            state_repository=state_repository,
        )

        request = CreateHomeRequest(
            name="HIOS Test Home",
            home_type="residential",
            description=(
                "Development home for HIOS integration testing."
            ),
            information=HomeInformationInput(
                country="Nigeria",
                city="Lagos",
                address="HIOS Test Address",
                postcode=None,
            ),
        )

        home = await service.create(
            subject_id=SUBJECT_ID,
            request=request,
        )

        print("Home created successfully")
        print(f"subject_id={SUBJECT_ID}")
        print(f"home_id={home.id}")


if __name__ == "__main__":
    asyncio.run(main())