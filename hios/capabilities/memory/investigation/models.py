from enum import StrEnum


class InvestigationMemoryCategory(StrEnum):
    QUESTION = "investigation_question"
    ANSWER = "investigation_answer"
    EVIDENCE_REQUEST = "investigation_evidence_request"
    EVIDENCE = "investigation_evidence"