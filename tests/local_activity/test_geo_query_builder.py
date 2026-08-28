import pytest

from hios.capabilities.local_activity.geo.query_builder import (
    GeoQueryBuilder,
)


def test_radius_to_wkt_creates_closed_polygon():

    builder = GeoQueryBuilder()

    geometry = builder.radius_to_wkt(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert geometry.startswith(
        "POLYGON(("
    )

    assert geometry.endswith(
        "))"
    )

    coordinates = geometry[
        len("POLYGON(("):-2
    ].split(",")

    assert len(coordinates) == 17

    assert coordinates[0] == coordinates[-1]


def test_radius_to_wkt_rejects_invalid_radius():

    builder = GeoQueryBuilder()

    with pytest.raises(ValueError):

        builder.radius_to_wkt(
            latitude=51.5074,
            longitude=-0.1278,
            radius_km=0,
        )


def test_radius_to_wkt_rejects_too_few_points():

    builder = GeoQueryBuilder()

    with pytest.raises(ValueError):

        builder.radius_to_wkt(
            latitude=51.5074,
            longitude=-0.1278,
            radius_km=5.0,
            points=3,
        )