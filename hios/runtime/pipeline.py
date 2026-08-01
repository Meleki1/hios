from __future__ import annotations

from dataclasses import dataclass

from hios.runtime.types import CapabilityType


@dataclass(frozen=True)
class PipelineStep:
    
    capability: CapabilityType
    required: bool = True
   

    


@dataclass(frozen=True)
class Pipeline:

    name: str
    steps: tuple[PipelineStep, ...]