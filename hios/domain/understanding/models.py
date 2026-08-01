from __future__ import annotations

from pydantic import Field

from hios.shared.entity import Entity

from .facts import Facts
from .hypotheses import Hypotheses
from .unknowns import Unknowns
from .summary import Summary
from .confidence import Confidence


class Understanding(Entity):
    """
    Represents the current understanding of a situation.

    Understanding evolves as new observations
    and expert opinions become available.
    """

    facts: Facts = Field(default_factory=Facts)

    hypotheses: Hypotheses = Field(default_factory=Hypotheses)

    unknowns: Unknowns = Field(default_factory=Unknowns)

    summary: Summary = Field(default_factory=Summary)

    confidence: Confidence = Field(default_factory=Confidence)