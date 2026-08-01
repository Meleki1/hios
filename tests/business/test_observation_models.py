from hios.domain.business.observation.models import Observation
from hios.domain.business.observation.observation_medium import (
    ObservationMedium,
)
from hios.domain.business.observation.observation_source import (
    ObservationSource,
)


def test_create_observation():
    observation = Observation(
        source=ObservationSource.USER,
        medium=ObservationMedium.TEXT,
        content="Mouse droppings found behind the sink.",
    )

    assert observation.content.startswith("Mouse")
    assert observation.is_text
    assert observation.is_user


def test_image_observation():
    observation = Observation(
        source=ObservationSource.CAMERA,
        medium=ObservationMedium.IMAGE,
        content="kitchen.jpg",
    )

    assert observation.is_image