"""JWT 签发与校验。"""

from datetime import UTC, datetime, timedelta
from typing import Any, Literal
from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError

from app.core.settings import settings

TokenType = Literal["access", "refresh"]


def create_access_token(*, user_id: str, org_id: str) -> str:
    """签发短时效 Access Token。"""
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.jwt_access_expire_minutes)
    payload: dict[str, Any] = {
        "sub": user_id,
        "org_id": org_id,
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(*, user_id: str, org_id: str) -> tuple[str, str, int]:
    """签发 Refresh Token，返回 (token, jti, ttl_seconds)。"""
    now = datetime.now(UTC)
    expire = now + timedelta(days=settings.jwt_refresh_expire_days)
    jti = str(uuid4())
    payload: dict[str, Any] = {
        "sub": user_id,
        "org_id": org_id,
        "type": "refresh",
        "jti": jti,
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    ttl_seconds = int((expire - now).total_seconds())
    return token, jti, ttl_seconds


def decode_token(token: str, *, expected_type: TokenType) -> dict[str, Any]:
    """解码并校验 Token 类型；失败抛 InvalidTokenError。"""
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    if payload.get("type") != expected_type:
        raise InvalidTokenError("token type mismatch")
    if not payload.get("sub"):
        raise InvalidTokenError("missing subject")
    return payload
