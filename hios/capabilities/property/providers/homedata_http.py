from typing import Any

import httpx

from hios.capabilities.property.providers.homedata_client import (
    HomedataClient,
)


class HttpHomedataClient(HomedataClient):

    BASE_URL = "https://api.homedata.co.uk/api"

    def __init__(
        self,
        api_key: str,
        timeout: float = 10.0,
        client: httpx.AsyncClient | None = None,
    ):
        self._api_key = api_key
        self._timeout = timeout
        self._client = client

    async def get_property(
        self,
        uprn: str,
    ) -> dict[str, Any]:

        headers = {
            "Authorization": f"Api-Key {self._api_key}",
        }

        url = (
            f"{self.BASE_URL}"
            f"/property/{uprn}/base"
        )

        if self._client is not None:
            response = await self._client.get(
                url,
                headers=headers,
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()