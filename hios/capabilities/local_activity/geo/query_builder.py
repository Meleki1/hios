from math import cos, pi


class GeoQueryBuilder:

    EARTH_RADIUS_KM = 6371.0

    def radius_to_wkt(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        points: int = 16,
    ) -> str:

        if radius_km <= 0:
            raise ValueError(
                "radius_km must be greater than 0"
            )

        if points < 4:
            raise ValueError(
                "points must be at least 4"
            )

        coordinates = []

        latitude_radius = (
            radius_km
            / self.EARTH_RADIUS_KM
        )

        longitude_radius = (
            radius_km
            / (
                self.EARTH_RADIUS_KM
                * cos(latitude * pi / 180)
            )
        )

        for index in range(points):

            angle = (
                2 * pi * index / points
            )

            lat = (
                latitude
                + latitude_radius
                * cos(angle)
                * 180
                / pi
            )

            lon = (
                longitude
                + longitude_radius
                * __import__("math").sin(angle)
                * 180
                / pi
            )

            coordinates.append(
                f"{lon} {lat}"
            )

        coordinates.append(
            coordinates[0]
        )

        return (
            "POLYGON(("
            + ",".join(coordinates)
            + "))"
        )