from pydantic import BaseModel, Field


class PropertyProfile(BaseModel):

    uprn: str | None = None

    address: str

    postcode: str | None = None

    year_built: int | None = None

    age_band: str | None = None

    property_type: str | None = None

    building_type: str | None = None

    construction_material: str | None = None

    bedrooms: int | None = None

    bathrooms: int | None = None

    floor_count: int | None = None

    floor_area: float | None = None

    has_basement: bool | None = None

    epc_rating: str | None = None

    epc_efficiency: int | None = None

    latitude: float | None = None

    longitude: float | None = None

    metadata: dict = Field(
        default_factory=dict,
    )