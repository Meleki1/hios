from typing import Any

import httpx

from hios.capabilities.property.providers.homedata_address_client import (
    HomedataAddressClient,
)


class HttpHomedataAddressClient(HomedataAddressClient):

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

    async def search(
        self,
        query: str,
    ) -> list[dict[str, Any]]:

        headers = {
            "Authorization": f"Api-Key {self._api_key}",
        }

        params = {
            "q": query,
        }

        url = (
            f"{self.BASE_URL}"
            "/address/find/"
        )

        if self._client is not None:
            response = await self._client.get(
                url,
                headers=headers,
                params=params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            data = response.json()

        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=self._timeout,
                )
                response.raise_for_status()
                data = response.json()

        return data.get("suggestions", [])