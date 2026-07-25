"""FastAPI 依赖注入集合。"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.run_repository import RunRepository
from app.services.run_service import RunService


def get_run_repository(db: AsyncSession = Depends(get_db)) -> RunRepository:
    """注入 RunRepository。"""
    return RunRepository(db)


def get_run_service(
    repository: RunRepository = Depends(get_run_repository),
) -> RunService:
    """注入 RunService。"""
    return RunService(repository)


__all__ = ["get_db", "get_run_repository", "get_run_service"]
