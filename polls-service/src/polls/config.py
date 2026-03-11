"""Application settings loaded from environment variables / .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    port: int = 8005

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
