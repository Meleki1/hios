from __future__ import annotations
from pydantic import Field
from hios.shared.base import HIOSModel
from hios.shared.identifier import EntityId
from hios.shared.audit import AuditInfo


class Entity(HIOSModel):
    
    id: EntityId = Field(default_factory=EntityId.new)

    audit: AuditInfo = Field(default_factory=AuditInfo)