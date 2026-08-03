"""认证业务逻辑。"""

from uuid import uuid4

from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from redis.asyncio import Redis

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.redis import refresh_token_key
from app.models import Users
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserPublic,
)
from app.utils.password import hash_password, verify_password

DEFAULT_ORG_ID = "default"


class AuthService:
    """注册 / 登录 / 刷新 / 登出。"""

    def __init__(self, repository: UserRepository, redis: Redis) -> None:
        self._repository = repository
        self._redis = redis

    @staticmethod
    def _to_public(user: Users) -> UserPublic:
        return UserPublic(
            id=user.id,
            org_id=user.org_id,
            username=user.username,
            created_at=user.created_at,
        )

    async def _issue_tokens(self, user: Users) -> tuple[TokenResponse, str, int]:
        """签发 access + refresh，并把 refresh jti 写入 Redis。"""
        access_token = create_access_token(user_id=user.id, org_id=user.org_id)
        refresh_token, jti, ttl_seconds = create_refresh_token(
            user_id=user.id,
            org_id=user.org_id,
        )
        await self._redis.set(refresh_token_key(jti), user.id, ex=ttl_seconds)
        return (
            TokenResponse(access_token=access_token, user=self._to_public(user)),
            refresh_token,
            ttl_seconds,
        )

    async def register(self, request: RegisterRequest) -> tuple[TokenResponse, str, int]:
        """注册并登录；用户名冲突返回 409。"""
        existing = await self._repository.get_by_username(request.username)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="用户名已存在",
            )

        user = Users(
            id=str(uuid4()),
            org_id=DEFAULT_ORG_ID,
            username=request.username,
            password_hash=hash_password(request.password),
        )
        created = await self._repository.create(user)
        return await self._issue_tokens(created)

    async def login(self, request: LoginRequest) -> tuple[TokenResponse, str, int]:
        """登录；失败统一 401。"""
        user = await self._repository.get_by_username(request.username)
        if user is None or not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
            )
        return await self._issue_tokens(user)

    async def refresh(self, refresh_token: str | None) -> tuple[TokenResponse, str, int]:
        """校验并轮转 Refresh Token。"""
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="缺少 refresh token",
            )

        try:
            payload = decode_token(refresh_token, expected_type="refresh")
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="refresh token 无效",
            ) from None

        jti = payload.get("jti")
        user_id = payload["sub"]
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="refresh token 无效",
            )

        stored_user_id = await self._redis.get(refresh_token_key(jti))
        if stored_user_id is None or stored_user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="refresh token 已失效",
            )

        # 轮转：先吊销旧 jti
        await self._redis.delete(refresh_token_key(jti))

        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
            )
        return await self._issue_tokens(user)

    async def logout(self, refresh_token: str | None) -> None:
        """吊销 Redis 中的 refresh jti。"""
        if not refresh_token:
            return
        try:
            payload = decode_token(refresh_token, expected_type="refresh")
        except InvalidTokenError:
            return
        jti = payload.get("jti")
        if jti:
            await self._redis.delete(refresh_token_key(jti))

    async def get_me(self, user_id: str) -> UserPublic:
        """获取当前用户。"""
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
            )
        return self._to_public(user)
