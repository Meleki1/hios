from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    database_url: str
    database_echo: bool = False

    openai_api_key: str
    assistant_model: str = "gpt-4o-mini"
    embedding_model: str = (
        "text-embedding-3-small"
    )

    image_diagnosis_model: str = (
        "gpt-5"
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

    telegram_bot_token: str
    telegram_webhook_secret: str
    telegram_default_subject_id: str
    telegram_default_home_id: str
    hios_bootstrap_secret: str
    


@lru_cache
def get_settings() -> Settings:

    return Settings()