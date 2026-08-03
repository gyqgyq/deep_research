import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.core.settings import settings
from app.db.redis import redis_client
from app.db.session import engine
from app.messaging import connect as rabbitmq_connect
from app.messaging import disconnect as rabbitmq_disconnect
from app.messaging import ping as rabbitmq_ping

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """应用生命周期：启动时探测数据库、Redis、RabbitMQ，关闭时释放连接。"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("postgres连接成功")
    except Exception:
        logger.exception("postgres连接失败")
        raise

    try:
        await redis_client.ping()
        logger.info("Redis 连接成功")
    except Exception:
        logger.exception("Redis 连接失败")
        raise

    try:
        await rabbitmq_connect()
        await rabbitmq_ping()
        logger.info("RabbitMQ 连接成功")
    except Exception:
        logger.exception("RabbitMQ 连接失败")
        raise

    yield

    await rabbitmq_disconnect()
    await redis_client.aclose()
    await engine.dispose()
    logger.info("连接池已释放")


def create_app() -> FastAPI:
    """应用工厂，便于测试与多实例创建。"""
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        """将领域异常转为 HTTP JSON 响应。"""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
