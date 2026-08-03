"""认证相关请求/响应模型。"""

from datetime import datetime

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """注册请求。"""

    username: str = Field(..., min_length=3, max_length=64, description="用户名")
    password: str = Field(..., min_length=8, max_length=128, description="密码")


class LoginRequest(BaseModel):
    """登录请求。"""

    username: str = Field(..., min_length=1, max_length=64, description="用户名")
    password: str = Field(..., min_length=1, max_length=128, description="密码")


class UserPublic(BaseModel):
    """对外暴露的用户摘要。"""

    id: str
    org_id: str
    username: str
    created_at: datetime


class TokenResponse(BaseModel):
    """Access Token 响应（Refresh 走 Cookie）。"""

    access_token: str
    token_type: str = "bearer"
    user: UserPublic
