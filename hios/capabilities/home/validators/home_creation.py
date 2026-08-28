from hios.capabilities.home.models.home_type import HomeType


class HomeCreationValidator:

    @staticmethod
    def validate(
        name: str,
        home_type: str,
    ) -> None:

        HomeCreationValidator.validate_name(
            name,
        )

        HomeCreationValidator.validate_home_type(
            home_type,
        )

    @staticmethod
    def validate_name(
        name: str,
    ) -> None:

        if not name.strip():
            raise ValueError(
                "Home name cannot be empty."
            )

    @staticmethod
    def validate_home_type(
        home_type: str,
    ) -> None:

        valid_types = {
            home_type.value
            for home_type in HomeType
        }

        if home_type not in valid_types:
            raise ValueError(
                f"Invalid home type: {home_type}"
            )