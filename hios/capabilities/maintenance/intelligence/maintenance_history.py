class MaintenanceHistorySignalExtractor:

    def extract(
        self,
        timeline,
    ) -> list[dict]:

        signals = []

        for entry in timeline or []:
            signals.append(
                {
                    "event_name": entry.event_name,
                    "description": entry.description,
                    "subject_id": entry.subject_id,
                    "resource_id": entry.resource_id,
                    "resource_type": entry.resource_type,
                    "created_at": entry.created_at,
                }
            )

        return signals