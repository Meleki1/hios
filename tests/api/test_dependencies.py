import pytest

from hios.api.dependencies import (
    get_geo_query_builder,
    get_planning_application_adapter,
    get_planning_application_mapper,
)
from hios.api.dependencies import (
    get_property_service,
)
from hios.api.dependencies import (
    get_environmental_service,
)
from hios.api.dependencies import (
    get_local_activity_service,
)
from hios.api.dependencies import (
    get_basic_signal_engine,
)
from hios.api.dependencies import (
    get_intent_scorer,
)
from hios.api.dependencies import (
    get_image_signal_collector,
)
from hios.api.dependencies import (
    get_signal_collection_service,
)
from hios.api.dependencies import (
    get_risk_assessment_service,
)
from hios.api.dependencies import (
    get_risk_signal_adapter,
)
from hios.api.dependencies import (
    get_prediction_evaluator, get_home_context_assembler, get_hios
)
from hios.api.dependencies import (
    get_prediction_evaluation_repository, get_home_property_service
)
from hios.api.dependencies import (
    get_intelligence_service, get_timeline_service, get_home_assistant_graph
)
from hios.api.dependencies import (
    get_intelligence_graph, get_maintenance_repository, get_memory_service
)
from hios.api.dependencies import (
    get_home_state_repository, get_home_information_repository, get_home_repository

)






def test_planning_dependencies_can_be_created():

    assert get_geo_query_builder() is not None
    assert get_planning_application_adapter() is not None
    assert get_planning_application_mapper() is not None

def test_property_service_can_be_created():

    service = get_property_service()

    assert service is not None

def test_environmental_service_can_be_created():

    service = get_environmental_service()

    assert service is not None

def test_local_activity_service_can_be_created():

    service = get_local_activity_service()

    assert service is not None

def test_basic_signal_engine_can_be_created():

    engine = get_basic_signal_engine()

    assert engine is not None

def test_intent_scorer_can_be_created():

    scorer = get_intent_scorer()

    assert scorer is not None

def test_image_signal_collector_can_be_created():

    collector = get_image_signal_collector()

    assert collector is not None

def test_signal_collection_service_can_be_created():

    service = get_signal_collection_service()

    assert service is not None

def test_risk_assessment_service_can_be_created():

    service = get_risk_assessment_service()

    assert service is not None

def test_risk_signal_adapter_can_be_created():

    adapter = get_risk_signal_adapter()

    assert adapter is not None

def test_prediction_evaluator_can_be_created():

    evaluator = get_prediction_evaluator()

    assert evaluator is not None

def test_prediction_evaluation_repository_can_be_created(
    session,
):
    repository = get_prediction_evaluation_repository(
        session
    )

    assert repository is not None

    assert repository is not None

def test_intelligence_service_can_be_created(
    session,
):
    service = get_intelligence_service(
        session,
    )

    assert service is not None

def test_intelligence_graph_can_be_created(
    session,
):
    graph = get_intelligence_graph(
        session,
    )

    assert graph is not None

def test_home_repository_can_be_created(
    session,
):
    repository = get_home_repository(
        session,
    )

    assert repository is not None


def test_home_information_repository_can_be_created(
    session,
):
    repository = get_home_information_repository(
        session,
    )

    assert repository is not None


def test_home_state_repository_can_be_created(
    session,
):
    repository = get_home_state_repository(
        session,
    )

    assert repository is not None

def test_maintenance_repository_can_be_created(
    session,
):
    repository = get_maintenance_repository(
        session,
    )

    assert repository is not None

def test_memory_service_can_be_created(
    session,
):
    service = get_memory_service(
        session,
    )

    assert service is not None

def test_timeline_service_can_be_created(
    session,
):
    service = get_timeline_service(
        session,
    )

    assert service is not None

def test_home_property_service_can_be_created(
    session,
):
    service = get_home_property_service(
        session,
    )

    assert service is not None

def test_home_context_assembler_can_be_created(
    session,
):
    assembler = get_home_context_assembler(session)

    assert assembler is not None

def test_hios_can_be_created():
    hios = get_hios()

    assert hios is not None
    assert hasattr(hios, "execute")

def test_home_assistant_graph_can_be_created(
    session,
):
    graph = get_home_assistant_graph(session)

    assert graph is not None