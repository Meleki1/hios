from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from hios.api.dependencies import get_db_session
from hios.core.config import get_settings
from hios.capabilities.home.repositories.home_repository import (
    HomeRepository,
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
from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)
from hios.capabilities.home.services.home_service import HomeService


router = APIRouter(
    prefix="/internal",
    tags=["internal"],
)


@router.post("/bootstrap/test-home")
async def bootstrap_test_home(
    x_hios_bootstrap_secret: str | None = Header(
        default=None,
    ),
    session: AsyncSession = Depends(
        get_db_session,
    ),
):
    settings = get_settings()

    if x_hios_bootstrap_secret != settings.hios_bootstrap_secret:
        raise HTTPException(
            status_code=403,
            detail="Invalid bootstrap secret",
        )

    home_repository: HomeRepository = (
        PostgresHomeRepository(
            session=session,
        )
    )

    information_repository = (
        PostgresHomeInformationRepository(
            session=session,
        )
    )

    state_repository = (
        PostgresHomeStateRepository(
            session=session,
        )
    )

    home_service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    existing_home = await home_repository.get(
        settings.telegram_default_home_id,
    )

    if existing_home is not None:
        return {
            "created": False,
            "subject_id": settings.telegram_default_subject_id,
            "home_id": existing_home.id,
        }

    home = await home_service.create(
        subject_id=settings.telegram_default_subject_id,
        request=CreateHomeRequest(
            name="HIOS Telegram Test Home",
            home_type="residential",
            description=(
                "Temporary home for HIOS Telegram integration testing."
            ),
            information=HomeInformationInput(
                country="Nigeria",
                city="Lagos",
                address="HIOS Telegram Test Address",
                postcode=None,
            ),
        ),
    )

    return {
        "created": True,
        "subject_id": settings.telegram_default_subject_id,
        "home_id": home.id,
    }