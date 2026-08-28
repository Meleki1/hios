from datetime import datetime, timedelta, timezone


class MaintenanceRecommendationScheduler:

    def schedule(
        self,
        *,
        now: datetime | None = None,
        horizon_days: int = 30
    ) -> datetime:
        if now is None:
            now = datetime.now(timezone.utc)

        return now + timedelta(days=horizon_days)