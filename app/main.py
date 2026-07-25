import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.core.settings import settings
from app.db.session import engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """应用生命周期：启动时探测数据库，关闭时释放连接池。"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("数据库连接成功")
    except Exception:
        logger.exception("数据库连接失败")
        raise
    yield
    await engine.dispose()
    logger.info("数据库连接池已释放")


def create_app() -> FastAPI:
    """应用工厂，便于测试与多实例创建。"""
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
