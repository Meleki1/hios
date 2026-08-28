from pydantic import BaseModel, Field


class HomeInformationInput(BaseModel):

    country: str

    city: str

    address: str

    postcode: str | None = None


class CreateHomeRequest(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=150,
    )

    home_type: str

    description: str | None = None

    information: HomeInformationInput