
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HelixDesk API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    database_url: str = (
        "postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/helixdesk"
    )
    test_database_url: str = (
        "postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/helixdesk_test"
    )

    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, gt=0, le=1440)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
