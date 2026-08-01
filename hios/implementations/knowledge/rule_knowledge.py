from hios.contracts.knowledge import KnowledgeCapability, KnowledgeRequest, KnowledgeResult



class RuleKnowledgeCapability(
    KnowledgeCapability,
):
    """
    Simple deterministic implementation.
    """

    async def execute(
        self,
        request: KnowledgeRequest,
        context,
    ) -> KnowledgeResult:

        return KnowledgeResult(
            knowledge="Knowledge acquired."
        )