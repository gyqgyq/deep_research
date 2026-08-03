"""认证相关路由。"""

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import (
    REFRESH_COOKIE_NAME,
    get_auth_service,
    get_current_user,
    get_refresh_token_from_cookie,
)
from app.core.settings import settings
from app.models import Users
from app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserPublic,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE_PATH = "/api/v1/auth"


def _set_refresh_cookie(response: Response, refresh_token: str, max_age: int) -> None:
    """写入 HttpOnly Refresh Cookie。"""
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite="lax",
        path=REFRESH_COOKIE_PATH,
        max_age=max_age,
    )


def _clear_refresh_cookie(response: Response) -> None:
    """清除 Refresh Cookie。"""
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
    )


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """注册并返回 Access Token；Refresh 写入 Cookie。"""
    token_response, refresh_token, ttl = await service.register(request)
    _set_refresh_cookie(response, refresh_token, ttl)
    return token_response


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """登录并返回 Access Token；Refresh 写入 Cookie。"""
    token_response, refresh_token, ttl = await service.login(request)
    _set_refresh_cookie(response, refresh_token, ttl)
    return token_response


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Depends(get_refresh_token_from_cookie),
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """用 Cookie 中的 Refresh Token 轮转签发新 Token。"""
    token_response, new_refresh, ttl = await service.refresh(refresh_token)
    _set_refresh_cookie(response, new_refresh, ttl)
    return token_response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    refresh_token: str | None = Depends(get_refresh_token_from_cookie),
    service: AuthService = Depends(get_auth_service),
) -> None:
    """吊销 Refresh Token 并清除 Cookie。"""
    await service.logout(refresh_token)
    _clear_refresh_cookie(response)


@router.get("/me", response_model=UserPublic)
async def me(
    current_user: Users = Depends(get_current_user),
) -> UserPublic:
    """返回当前登录用户。"""
    return UserPublic(
        id=current_user.id,
        org_id=current_user.org_id,
        username=current_user.username,
        created_at=current_user.created_at,
    )
