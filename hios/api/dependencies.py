from fastapi import Depends, Request
from hios.capabilities.assistant.chat import (
    HomeAssistantChat,
)
from hios.capabilities.assistant.router.default_interaction_router import (
    DefaultInteractionRouter,
)
from hios.capabilities.intelligence.graph.workflow import (
    build_intelligence_graph,
)
import httpx
from hios.core.config import get_settings
from hios.capabilities.environmental.providers.weather_client import (
    WeatherHttpClient,
)

from hios.capabilities.local_activity.clients.planning_data_http_client import (
    PlanningDataHTTPClient,
)

from hios.capabilities.property.providers.homedata_http import (
    HttpHomedataClient,
)
from hios.capabilities.local_activity.providers.planning_application_adapter import (
    PlanningApplicationAdapter,
)

from hios.capabilities.local_activity.mappers.planning_application_mapper import (
    PlanningApplicationMapper,
)

from hios.capabilities.local_activity.geo.query_builder import (
    GeoQueryBuilder,
)
from hios.capabilities.property.service import (
    PropertyService,
)

from hios.capabilities.property.providers.homedata import (
    HomedataProvider,
)
from hios.capabilities.environmental.service import (
    EnvironmentalService,
)

from hios.capabilities.environmental.providers.weather import (
    WeatherProvider,
)
from hios.capabilities.local_activity.local_activity_service import (
    LocalActivityService,
)

from hios.capabilities.local_activity.providers.planning_activity_provider import (
    PlanningActivityProvider,
)
from hios.capabilities.intelligence.collectors.explicit_intent import (
    ExplicitIntentCollector,
)
from hios.capabilities.intelligence.collectors.conversation import (
    ConversationSignalCollector,
)
from hios.capabilities.intelligence.collectors.property import (
    PropertySignalCollector,
)
from hios.capabilities.intelligence.collectors.environmental import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)
from hios.capabilities.local_activity.local_activity_aggregator import (
    LocalActivityAggregator,
)
from hios.capabilities.intelligence.collectors.platform import (
    PlatformBehaviourSignalCollector,
)
from hios.capabilities.intelligence.basic_signal_engine import (
    BasicSignalEngine,
)
from hios.capabilities.intelligence.rule_based_intent_scorer import (
    RuleBasedIntentScorer,
)
from hios.capabilities.image_diagnosis.services.image_signal_collector import (
    ImageSignalCollector,
)
from hios.capabilities.intelligence.signal_collection_service import (
    SignalCollectionService,
)
from hios.capabilities.risk.risk_engine import RiskEngine

from hios.capabilities.risk.risk_service import (
    RiskService,
)

from hios.capabilities.risk.risk_assessment_service import (
    RiskAssessmentService,
)

from hios.capabilities.risk.rule_based_risk_engine import (
    RuleBasedRiskEngine,
)
from hios.capabilities.risk.risk_signal_adapter import (
    RiskSignalAdapter,
)
from hios.capabilities.intelligence.basic_prediction_engine import (
    BasicPredictionEngine,
)
from hios.capabilities.intelligence.prediction_engine import (
    PredictionEngine,
)
from hios.capabilities.intelligence.basic_prediction_evaluator import (
    BasicPredictionEvaluator,
)
from hios.capabilities.intelligence.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)
from hios.capabilities.intelligence.postgres.prediction_evaluation_repository import (
    PostgresPredictionEvaluationRepository,
)
from hios.capabilities.intelligence.postgres.prediction_repository import (
    PostgresPredictionRepository,
)
from hios.capabilities.home.repositories.postgres_home_repository import (
    PostgresHomeRepository,
)
from hios.capabilities.home.repositories.postgres_home_information_repository import (
    PostgresHomeInformationRepository,
)
from hios.capabilities.home.repositories.postgres_home_state_repository import (
    PostgresHomeStateRepository,
)
from hios.capabilities.maintenance.postgres.maintenance_repository import (
    PostgresMaintenanceRepository,
)
from hios.capabilities.memory.service import MemoryService
from hios.capabilities.memory.formation import MemoryFormation
from hios.capabilities.memory.rule_based_formation import RuleBasedMemoryFormation

from hios.capabilities.memory.store import MemoryStore
from hios.capabilities.memory.postgres import PostgresMemoryStore

from hios.capabilities.memory.deduplication import MemoryDeduplicator
from hios.capabilities.memory.postgres_deduplication import (
    PostgresMemoryDeduplicator,
)
from hios.capabilities.timeline.services.timeline_service import TimelineService
from hios.capabilities.timeline.repositories.postgres_timeline_repository import (
    PostgresTimelineRepository,
)
from hios.capabilities.home.services.home_property_service import (
    HomePropertyService,
)

from hios.capabilities.home.repositories.postgres_home_property_reference_repository import (
    PostgresHomePropertyReferenceRepository,
)
from hios.capabilities.assistant.graph.workflow import (
    build_home_assistant_graph,
)
from hios.capabilities.assistant.llm.openai import (
    OpenAIAssistantLLM,
)
from hios.capabilities.assistant.services.interaction_understanding import AssistantInteractionUnderstandingService
from hios.capabilities.assistant.services.response_generation import AssistantResponseGenerationService
from hios.runtime.hios import HIOS
from hios.capabilities.assistant.context.home_context_assembler import HomeContextAssembler
from hios.db.repositories.memory_repository import MemoryRepository
from hios.capabilities.memory.embedding import OpenAIEmbedder
from hios.capabilities.intelligence.intelligence_service import IntelligenceService
from hios.capabilities.intelligence.prediction_service import PredictionService
from sqlalchemy.ext.asyncio import AsyncSession
from hios.packs.pest_control.builder import (
    create as create_pest_control_hios,
)
from hios.capabilities.assistant.telegram.client import (
    TelegramClient,
)
from hios.capabilities.assistant.telegram.webhook import (
    TelegramWebhookHandler,
)
from hios.capabilities.assistant.telegram.provisioning import (
    TelegramProvisioningService,
)
from hios.capabilities.home.services.home_service import (
    HomeService,
)

from hios.capabilities.home.repositories.postgres_home_repository import (
    PostgresHomeRepository,
)

from hios.capabilities.home.repositories.postgres_home_information_repository import (
    PostgresHomeInformationRepository,
)

from hios.capabilities.home.repositories.postgres_home_state_repository import (
    PostgresHomeStateRepository,
)
from hios.db.session import SessionLocal


_http_client: httpx.AsyncClient | None = None

async def get_db_session():
    async with SessionLocal() as session:
        yield session

def get_http_client() -> httpx.AsyncClient:
    global _http_client

    if _http_client is None:
        _http_client = httpx.AsyncClient()

    return _http_client


def get_weather_client() -> WeatherHttpClient:
    return WeatherHttpClient(
        client=get_http_client(),
    )


def get_planning_data_client() -> PlanningDataHTTPClient:
    return PlanningDataHTTPClient(
        client=get_http_client(),
    )


def get_homedata_client() -> HttpHomedataClient:
    settings = get_settings()

    return HttpHomedataClient(
        api_key=settings.homedata_api_key,
        client=get_http_client(),
    )

def get_planning_application_adapter() -> PlanningApplicationAdapter:
    return PlanningApplicationAdapter()


def get_planning_application_mapper() -> PlanningApplicationMapper:
    return PlanningApplicationMapper()


def get_geo_query_builder() -> GeoQueryBuilder:
    return GeoQueryBuilder()

def get_property_service() -> PropertyService:
    provider = HomedataProvider(
        client=get_homedata_client(),
    )

    return PropertyService(
        provider=provider,
    )

def get_environmental_service() -> EnvironmentalService:
    provider = WeatherProvider(
        client=get_weather_client(),
    )

    return EnvironmentalService(
        provider=provider,
    )

def get_local_activity_service() -> LocalActivityService:
    provider = PlanningActivityProvider(
        client=get_planning_data_client(),
        geo_query_builder=get_geo_query_builder(),
        adapter=get_planning_application_adapter(),
        mapper=get_planning_application_mapper(),
    )

    return LocalActivityService(
        providers=[provider],
    )

def get_basic_signal_engine() -> BasicSignalEngine:
    return BasicSignalEngine(
        explicit_intent_collector=ExplicitIntentCollector(),
        conversation_collector=ConversationSignalCollector(),
        property_collector=PropertySignalCollector(),
        environmental_collector=EnvironmentalSignalCollector(),
        local_activity_collector=LocalActivitySignalCollector(),
        platform_behaviour_collector=PlatformBehaviourSignalCollector(),
    )

def get_intent_scorer() -> RuleBasedIntentScorer:
    return RuleBasedIntentScorer()

def get_image_signal_collector() -> ImageSignalCollector:
    return ImageSignalCollector()

def get_signal_collection_service() -> SignalCollectionService:
    return SignalCollectionService(
        signal_engine=get_basic_signal_engine(),
        intent_scorer=get_intent_scorer(),
        property_service=get_property_service(),
        environmental_service=get_environmental_service(),
        local_activity_service=get_local_activity_service(),
        local_activity_aggregator=LocalActivityAggregator(),
        local_activity_signal_collector=LocalActivitySignalCollector(),
        image_signal_collector=ImageSignalCollector(),
    )

def get_risk_engine() -> RiskEngine:
    return RuleBasedRiskEngine()

def get_risk_service() -> RiskService:
    return RiskService(
        engine=get_risk_engine(),
    )

def get_risk_assessment_service() -> RiskAssessmentService:
    return RiskAssessmentService(
        risk_service=get_risk_service(),
    )

def get_risk_signal_adapter() -> RiskSignalAdapter:
    return RiskSignalAdapter()

def get_prediction_engine() -> PredictionEngine:
    return BasicPredictionEngine()

def get_prediction_evaluator() -> BasicPredictionEvaluator:
    return BasicPredictionEvaluator()

def get_prediction_evaluation_repository(
    session: AsyncSession,
) -> PredictionEvaluationRepository:
    return PostgresPredictionEvaluationRepository(
        session=session,
    )

def get_prediction_service(
    session: AsyncSession,
) -> PredictionService:
    return PredictionService(
        engine=get_prediction_engine(),
        repository=PostgresPredictionRepository(
            session=session,
        ),
    )

def get_intelligence_service(
    session: AsyncSession,
) -> IntelligenceService:
    return IntelligenceService(
        prediction_service=get_prediction_service(
            session,
        ),
        evaluator=get_prediction_evaluator(),
        evaluation_repository=PostgresPredictionEvaluationRepository(
            session=session,
        ),
    )

def get_intelligence_graph(
    session: AsyncSession,
):
    return build_intelligence_graph(
        signal_collection_service=get_signal_collection_service(),
        intelligence_service=get_intelligence_service(session),
        risk_assessment_service=get_risk_assessment_service(),
        risk_signal_adapter=get_risk_signal_adapter(),
    )

def get_home_repository(
    session: AsyncSession,
) -> PostgresHomeRepository:
    return PostgresHomeRepository(
        session=session,
    )


def get_home_information_repository(
    session: AsyncSession,
) -> PostgresHomeInformationRepository:
    return PostgresHomeInformationRepository(
        session=session,
    )


def get_home_state_repository(
    session: AsyncSession,
) -> PostgresHomeStateRepository:
    return PostgresHomeStateRepository(
        session=session,
    )

def get_maintenance_repository(
    session: AsyncSession,
) -> PostgresMaintenanceRepository:
    return PostgresMaintenanceRepository(
        session=session,
    )

def get_memory_service(
    session: AsyncSession,
) -> MemoryService:
    settings = get_settings()

    repository = MemoryRepository(
        session=session,
    )

    embedder = OpenAIEmbedder(
        api_key=settings.openai_api_key,
    )

    store = PostgresMemoryStore(
        repository=repository,
        embedder=embedder,
    )

    deduplicator = PostgresMemoryDeduplicator(
        repository=repository,
        embedder=embedder,
    )

    return MemoryService(
        store=store,
        formation=RuleBasedMemoryFormation(),
        deduplicator=deduplicator,
    )

def get_timeline_service(
    session: AsyncSession,
) -> TimelineService:
    return TimelineService(
        repository=PostgresTimelineRepository(
            session=session,
        ),
    )

def get_home_property_service(
    session: AsyncSession,
) -> HomePropertyService:
    return HomePropertyService(
        repository=PostgresHomePropertyReferenceRepository(
            session=session,
        ),
    )

def get_home_context_assembler(
    session: AsyncSession,
) -> HomeContextAssembler:
    return HomeContextAssembler(
        home_repository=get_home_repository(session),
        information_repository=get_home_information_repository(session),
        state_repository=get_home_state_repository(session),
        maintenance_repository=get_maintenance_repository(session),
        property_service=get_property_service(),
        memory_service=get_memory_service(session),
        timeline_service=get_timeline_service(session),
        home_property_service=get_home_property_service(session),
    )

def get_hios():
    return create_pest_control_hios()

def get_checkpointer(request: Request):
    return request.app.state.checkpointer

def get_home_assistant_graph(
    session: AsyncSession,
    checkpointer,
):
    return build_home_assistant_graph(
        checkpointer=checkpointer,
        context_assembler=get_home_context_assembler(session),
        router=DefaultInteractionRouter(
            llm=get_assistant_llm(),
        ),
        hios=get_hios(),
        intelligence_graph=get_intelligence_graph(session),
        response_generation_service=(
            get_assistant_response_generation_service()
        ),
        interaction_understanding_service=(
            get_interaction_understanding_service()
        ),
    )
    
def get_home_assistant_chat(
    session: AsyncSession = Depends(get_db_session),
    checkpointer=Depends(get_checkpointer),
) -> HomeAssistantChat:
    return HomeAssistantChat(
        graph=get_home_assistant_graph(
            session,
            checkpointer,
            ),
    )

def get_telegram_client() -> TelegramClient:
    settings = get_settings()

    return TelegramClient(
        bot_token=settings.telegram_bot_token,
        http_client=get_http_client(),
    )


def get_telegram_webhook_handler(
    session: AsyncSession = Depends(
        get_db_session,
    ),
) -> TelegramWebhookHandler:
    settings = get_settings()

    home_repository = PostgresHomeRepository(
        session=session,
    )

    information_repository = PostgresHomeInformationRepository(
        session=session,
    )

    state_repository = PostgresHomeStateRepository(
        session=session,
    )

    home_service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    provisioning_service = TelegramProvisioningService(
        home_service=home_service,
        home_repository=home_repository,
        subject_id=settings.telegram_default_subject_id,
        home_id=settings.telegram_default_home_id,
    )

    return TelegramWebhookHandler(
        assistant=get_home_assistant_chat(session),
        telegram=get_telegram_client(),
        provisioning_service=provisioning_service,
    )

def get_assistant_llm() -> OpenAIAssistantLLM:
    settings = get_settings()

    return OpenAIAssistantLLM(
        api_key=settings.openai_api_key,
        model=settings.assistant_model,
    )

def get_assistant_response_generation_service():
    return AssistantResponseGenerationService(
        llm=get_assistant_llm(),
    )

def get_interaction_understanding_service(
) -> AssistantInteractionUnderstandingService:
    return AssistantInteractionUnderstandingService(
        llm=get_assistant_llm(),
    )

