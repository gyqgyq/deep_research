"""FastAPI 依赖注入集合。"""

from app.db.session import get_db

__all__ = ["get_db"]
