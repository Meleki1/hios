from typing import Any

import httpx


class TelegramClient:

    def __init__(
        self,
        *,
        bot_token: str,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._bot_token = bot_token
        self._http_client = http_client

    @property
    def _base_url(self) -> str:
        return (
            f"https://api.telegram.org/"
            f"bot{self._bot_token}"
        )

    async def send_message(
        self,
        *,
        chat_id: int,
        text: str,
    ) -> dict[str, Any]:

        response = await self._http_client.post(
            f"{self._base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
        )

        response.raise_for_status()

        return response.json()

    async def set_webhook(
        self,
        *,
        url: str,
        secret_token: str | None = None,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "url": url,
        }

        if secret_token is not None:
            payload["secret_token"] = secret_token

        response = await self._http_client.post(
            f"{self._base_url}/setWebhook",
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    async def delete_webhook(self) -> dict[str, Any]:
        
        response = await self._http_client.post(
            f"{self._base_url}/deleteWebhook",
        )

        response.raise_for_status()

        return response.json()