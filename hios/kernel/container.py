from __future__ import annotations

from typing import Any


class ServiceContainer:
    """
    Stores framework services.

    Services are registered by type and resolved later.
    """

    def __init__(self) -> None:
        self._services: dict[type, Any] = {}

    def register(
        self,
        service_type: type,
        instance: Any,
    ) -> None:
        """
        Register a singleton service.
        """

        self._services[service_type] = instance

    def resolve(
        self,
        service_type: type,
    ) -> Any:
        """
        Resolve a registered service.
        """

        if service_type not in self._services:
            raise LookupError(
                f"{service_type.__name__} has not been registered."
            )

        return self._services[service_type]

    def contains(
        self,
        service_type: type,
    ) -> bool:
        return service_type in self._services

    def clear(self) -> None:
        self._services.clear()