from __future__ import annotations

from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.runtime.types import CapabilityType
from hios.shared.base import HIOSModel


class TraceEntry(HIOSModel):
    """
    One capability execution.
    """

    capability: CapabilityType

    request: CapabilityRequest

    result: CapabilityResult