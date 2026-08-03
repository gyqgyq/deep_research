from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.db_url import normalize_database_url

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

    # Redis
    redis_host: str
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 15
    jwt_refresh_expire_days: int = 7

    # Refresh Cookie：生产环境应开启 Secure
    cookie_secure: bool | None = None

    @field_validator("async_database_url")
    @classmethod
    def _normalize_database_url(cls, value: str) -> str:
        return normalize_database_url(value)

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def refresh_cookie_secure(self) -> bool:
        """Cookie Secure 标志：显式配置优先，否则生产环境为 True。"""
        if self.cookie_secure is not None:
            return self.cookie_secure
        return self.is_production

    @property
    def redis_url(self) -> str:
        """组装 Redis URL。"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache
def get_settings() -> Settings:
    """缓存 Settings 单例，便于测试时 clear_cache。"""
    return Settings()


settings = get_settings()
