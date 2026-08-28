import pytest
from tests.assistant.test_nodes import FakeRouter, FakeHIOS, FakeIntelligenceGraph, FakeContextAssembler, AssistantActionResponseBuilder
from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.maintenance.models.maintenance_recommendation import MaintenanceRecommendation
from tests.assistant.test_assistant_maintenance_intelligence import FakeMaintenanceIntelligence
from hios.capabilities.outreach.contracts import OutreachResult
from hios.capabilities.outreach.models import OutreachChannel, OutreachDeliveryStatus

class FakeOutreach:

    def __init__(self):
        self.requests = []

    async def reason(
        self,
        request,
        context,
    ):
        self.requests.append(request)

        return OutreachResult(
            status=OutreachDeliveryStatus.SENT,
            channel=OutreachChannel.EMAIL,
            recipient=request.recipient,
            message_id="fake-message-id",
        )

@pytest.mark.asyncio
async def test_no_maintenance_recommendation_does_not_require_outreach():

    intelligence_graph = FakeIntelligenceGraph()
    fake_hios = FakeHIOS()
    maintenance_intelligence = FakeMaintenanceIntelligence()
    

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=fake_hios,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=maintenance_intelligence,
        action_response_builder=AssistantActionResponseBuilder(),
    )


    result = await nodes["decide_outreach"]({
        "maintenance_recommendations": [],
    })

    decision = result["outreach_decision"]

    assert decision.required is False

@pytest.mark.asyncio
async def test_high_priority_maintenance_requires_outreach():

    intelligence_graph = FakeIntelligenceGraph()
    fake_hios = FakeHIOS()
    maintenance_intelligence = FakeMaintenanceIntelligence()
    

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=fake_hios,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=maintenance_intelligence,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    recommendation = MaintenanceRecommendation(
        subject_id="subject-123",
        home_id="home-123",
        task="Inspect roof",
        reason="Roof inspection is overdue.",
        maintenance_type="roof",
        priority="high",
    )

    result = await nodes["decide_outreach"]({
        "maintenance_recommendations": [
            recommendation,
        ],
    })

    decision = result["outreach_decision"]

    assert decision.required is True
    assert decision.priority == "high"