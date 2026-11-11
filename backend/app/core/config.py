from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# El .env vive en la raíz del repositorio (backend/app/core/config.py → raíz).
ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )

    project_name: str = "Agentic ServiceDesk API"
    api_prefix: str = "/v1"


settings = Settings()
