from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_user: str = "copilot"
    postgres_password: str
    postgres_db: str = "copilot"
    postgres_host: str = "localhost"
    postgres_port: int = 5432


@lru_cache
def get_settings() -> Settings:
    return Settings()
