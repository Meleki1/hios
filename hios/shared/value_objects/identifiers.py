from typing import NewType
from uuid import UUID

HomeId = NewType("HomeId", UUID)

CaseId = NewType("CaseId", UUID)

RoomId = NewType("RoomId", UUID)

AssetId = NewType("AssetId", UUID)

ObservationId = NewType("ObservationId", UUID)

EvidenceId = NewType("EvidenceId", UUID)

RecommendationId = NewType("RecommendationId", UUID)

TimelineEventId = NewType("TimelineEventId", UUID)