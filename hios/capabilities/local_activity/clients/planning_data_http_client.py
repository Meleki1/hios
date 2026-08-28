from typing import Any

import httpx


class PlanningDataHTTPClient:

    BASE_URL = (
        "https://www.planning.data.gov.uk/entity.json"
    )

    RETRYABLE_STATUS_CODES = {
        429,
        500,
        502,
        503,
        504,
    }

    def __init__(
        self,
        client: httpx.AsyncClient,
        max_retries: int = 2,
    ):
        if max_retries < 0:
            raise ValueError(
                "max_retries must be greater than or equal to 0"
            )

        self._client = client
        self._max_retries = max_retries

    async def _request(
        self,
        params: dict[str, Any],
    ) -> dict[str, Any]:

        for attempt in range(
            self._max_retries + 1
        ):

            response = await self._client.get(
                self.BASE_URL,
                params=params,
            )

            if (
                response.status_code
                not in self.RETRYABLE_STATUS_CODES
            ):
                response.raise_for_status()

                return response.json()

            if attempt >= self._max_retries:
                response.raise_for_status()

        raise RuntimeError(
            "Planning data request failed"
        )

    async def search(
        self,
        geometry: str,
        start_date_year: int | None = None,
        start_date_month: int | None = None,
        start_date_day: int | None = None,
        limit: int = 100,
        offset: int = 0,
        max_pages: int = 10,
    ) -> list[dict[str, Any]]:

        if limit <= 0:
            raise ValueError(
                "limit must be greater than 0"
            )

        if offset < 0:
            raise ValueError(
                "offset must be greater than or equal to 0"
            )

        if max_pages <= 0:
            raise ValueError(
                "max_pages must be greater than 0"
            )

        results: list[dict[str, Any]] = []

        for page in range(max_pages):

            current_offset = (
                offset + page * limit
            )

            params: dict[str, Any] = {
                "dataset": "planning-application",
                "geometry": geometry,
                "geometry_relation": "intersects",
                "limit": limit,
                "offset": current_offset,
            }

            if start_date_year is not None:
                params["start_date_year"] = (
                    start_date_year
                )
                params["start_date_match"] = "since"

            if start_date_month is not None:
                params["start_date_month"] = (
                    start_date_month
                )

            if start_date_day is not None:
                params["start_date_day"] = (
                    start_date_day
                )

            data = await self._request(
                params,
            )

            entities = data.get(
                "entities",
                [],
            )

            results.extend(
                entities,
            )

            if len(entities) < limit:
                break

        return results