import pytest

from hios.packs.pest_control.builder import create

from hios.capabilities.pest_control.models.request import PestControlRequest


@pytest.mark.asyncio
async def test_pest_control_pack():

    hios = create()

    result = await hios.execute(
        PestControlRequest(
            subject_id="subject-123",
            home_id="home-123",
            message=(
                "I found droppings and "
                "hear scratching around my kitchen."
            ),
        )
    )

    assert result is not None