from hios.capabilities.knowledge.contract import (
    KnowledgeCapability,
    KnowledgeRequest,
    KnowledgeResult,
)


class RuleKnowledgeCapability(
    KnowledgeCapability,
):
    """
    Deterministic implementation of the Knowledge capability.
    """

    async def execute(
        self,
        request: KnowledgeRequest,
        context,
    ) -> KnowledgeResult:

        return KnowledgeResult(
            facts=[
                "Knowledge acquired.",
            ]
        )