from abc import ABC

from hios.contracts.capability import Capability
from hios.capabilities.execution.contract import ExecutionRequest,ExecutionResult

class ExecutionCapability(
    Capability[
        ExecutionRequest,
        ExecutionResult,
    ],
    ABC,
):
    pass