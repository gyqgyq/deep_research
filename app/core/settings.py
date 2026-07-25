from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.db.url import normalize_database_url

# 项目根目录（backend/）
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """应用配置，从环境变量 / .env 读取。"""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Deep Research API"
    app_env: str = Field(default="development", description="运行环境：development / staging / production")
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    async_database_url: str
    dashscope_api_key: str

    @field_validator("async_database_url")
    @classmethod
    def _normalize_database_url(cls, value: str) -> str:
        return normalize_database_url(value)

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """缓存 Settings 单例，便于测试时 clear_cache。"""
    return Settings()


settings = get_settings()
