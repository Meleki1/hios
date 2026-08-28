from datetime import datetime, timedelta, timezone

from hios.capabilities.maintenance.services.maintenance_recommendation_scheduler import (
    MaintenanceRecommendationScheduler,
)
from hios.capabilities.maintenance.services.maintenance_recommendation_scheduler import (
    MaintenanceRecommendationScheduler,
)


def test_scheduler_returns_date_30_days_in_future():
    scheduler = MaintenanceRecommendationScheduler()

    now = datetime.now(timezone.utc)

    recommended_for = scheduler.schedule(
        now=now,
    )

    assert recommended_for == now + timedelta(days=30)



def test_scheduler_uses_requested_horizon():
    scheduler = MaintenanceRecommendationScheduler()

    now = datetime.now(timezone.utc)

    recommended_for = scheduler.schedule(
        now=now,
        horizon_days=7,
    )

    assert recommended_for == now + timedelta(days=7)