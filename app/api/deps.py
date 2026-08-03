"""FastAPI 依赖注入集合。"""

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.redis import redis_client
from app.db.session import get_db
from app.models import Users
from app.repositories.run_repository import RunRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.run_service import RunService

_bearer_scheme = HTTPBearer(auto_error=False)

REFRESH_COOKIE_NAME = "refresh_token"


def get_redis() -> Redis:
    """注入 Redis 客户端。"""
    return redis_client


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """注入 UserRepository。"""
    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
    redis: Redis = Depends(get_redis),
) -> AuthService:
    """注入 AuthService。"""
    return AuthService(repository, redis)


def get_run_repository(db: AsyncSession = Depends(get_db)) -> RunRepository:
    """注入 RunRepository。"""
    return RunRepository(db)


def get_run_service(
    repository: RunRepository = Depends(get_run_repository),
) -> RunService:
    """注入 RunService。"""
    return RunService(repository)


def get_refresh_token_from_cookie(
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE_NAME)] = None,
) -> str | None:
    """从 Cookie 读取 Refresh Token。"""
    return refresh_token


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(_bearer_scheme),
    ] = None,
    repository: UserRepository = Depends(get_user_repository),
) -> Users:
    """解析 Bearer Access Token 并返回当前用户。"""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供有效的 access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(credentials.credentials, expected_type="access")
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="access token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = await repository.get_by_id(payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


__all__ = [
    "get_db",
    "get_redis",
    "get_user_repository",
    "get_auth_service",
    "get_run_repository",
    "get_run_service",
    "get_refresh_token_from_cookie",
    "get_current_user",
]
