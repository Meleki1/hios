from hios.capabilities.local_activity.local_activity_provider import (
    LocalActivityProvider,
)

from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)

from hios.capabilities.local_activity.clients.planning_data_http_client import (
    PlanningDataHTTPClient,
)

from hios.capabilities.local_activity.geo.query_builder import (
    GeoQueryBuilder,
)

from hios.capabilities.local_activity.providers.planning_application_adapter import (
    PlanningApplicationAdapter,
)

from hios.capabilities.local_activity.mappers.planning_application_mapper import (
    PlanningApplicationMapper,
)


class PlanningActivityProvider(
    LocalActivityProvider,
):

    def __init__(
        self,
        client: PlanningDataHTTPClient,
        geo_query_builder: GeoQueryBuilder,
        adapter: PlanningApplicationAdapter,
        mapper: PlanningApplicationMapper,
    ):
        self._client = client
        self._geo_query_builder = geo_query_builder
        self._adapter = adapter
        self._mapper = mapper

    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[LocalActivityEvent]:

        geometry = (
            self._geo_query_builder.radius_to_wkt(
                latitude=latitude,
                longitude=longitude,
                radius_km=radius_km,
            )
        )

        raw_records = await self._client.search(
            geometry=geometry,
        )

        applications = [
            self._adapter.from_raw(
                record,
            )
            for record in raw_records
        ]

        return [
            self._mapper.to_event(
                application,
            )
            for application in applications
        ]