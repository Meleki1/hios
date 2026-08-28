from __future__ import annotations
from dataclasses import dataclass
from hios.runtime.types import CapabilityType
from hios.runtime.hooks.base import PipelineHook


@dataclass(frozen=True)
class PipelineStep:
    
    capability: CapabilityType
    required: bool = True
   

    


@dataclass(frozen=True)
class Pipeline:

    name: str
    steps: tuple[PipelineStep, ...]
    before_hooks: tuple[PipelineHook, ...] = ()
    after_hooks: tuple[PipelineHook, ...] = ()