from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    database_url: str
    database_echo: bool = False

    openai_api_key: str

    embedding_model: str = (
        "text-embedding-3-small"
    )

    image_diagnosis_model: str = (
        "gpt-4o-mini"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    email_host: str | None = None
    email_port: int = 587
    email_username: str | None = None
    email_password: str | None = None
    email_from: str | None = None
    email_use_tls: bool = True

    hios_test_email: str

    homedata_api_key: str


@lru_cache
def get_settings() -> Settings:

    return Settings()