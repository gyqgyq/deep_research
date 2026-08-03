"""领域异常：由 service 抛出，在 HTTP 层统一转换为响应。"""


class AppError(Exception):
    """业务异常基类。"""

    def __init__(self, message: str, *, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UnauthorizedError(AppError):
    """未认证或凭证无效。"""

    def __init__(self, message: str = "未授权") -> None:
        super().__init__(message, status_code=401)


class ConflictError(AppError):
    """资源冲突（如用户名已存在）。"""

    def __init__(self, message: str = "资源冲突") -> None:
        super().__init__(message, status_code=409)


class NotFoundError(AppError):
    """资源不存在。"""

    def __init__(self, message: str = "资源不存在") -> None:
        super().__init__(message, status_code=404)
