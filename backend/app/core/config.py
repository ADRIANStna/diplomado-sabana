from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    project_name: str = "Diplomado Sabana API"
    api_v1_prefix: str = "/api"


settings = Settings()
