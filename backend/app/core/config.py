from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    system_name: str = "Enterprise Canteen Operations System"
    app_version: str = "0.1.0"
    app_env: str = "local"
    database_url: str = "postgresql://canteen_user:canteen_password@postgres:5432/canteen_ops"
    ai_provider: str = "mock"
    ai_api_key: str = ""
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    log_level: str = "INFO"
    cors_origins_raw: str = "http://localhost:3100"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
