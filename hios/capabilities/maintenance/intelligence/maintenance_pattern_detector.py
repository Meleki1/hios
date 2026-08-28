from hios.capabilities.maintenance.models.maintenance_pattern import (
    MaintenancePattern,
)


class MaintenancePatternDetector:

    def detect(
        self,
        signals: list[dict],
    ) -> list[MaintenancePattern]:

        categories: dict[str, list[str]] = {
            "pest": [],
            "damp": [],
            "insulation": [],
            "roof": [],
            "gutter": [],
            "garden": [],
        }

        for signal in signals:
            description = (
                signal.get("description") or ""
            ).lower()

            if any(
                word in description
                for word in (
                    "mice",
                    "mouse",
                    "wasp",
                    "wasps",
                    "pest",
                )
            ):
                categories["pest"].append(
                    signal["description"]
                )

            if any(
                word in description
                for word in (
                    "damp",
                    "moisture",
                    "mould",
                    "mold",
                )
            ):
                categories["damp"].append(
                    signal["description"]
                )

            if any(
                word in description
                for word in (
                    "loft insulation",
                    "insulation",
            )
            ):
                categories["insulation"].append(
                    signal["description"]
                )

        patterns = []

        for category, descriptions in categories.items():

            if not descriptions:
                continue

            patterns.append(
                MaintenancePattern(
                    category=category,
                    occurrences=len(descriptions),
                    descriptions=descriptions,
                    confidence=min(
                        1.0,
                        len(descriptions) / 3,
                    ),
                )
            )

        return patterns