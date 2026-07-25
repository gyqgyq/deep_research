import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.routers.run_router import router as run_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
#     try:
#         async with engine.connect() as conn:
#             await conn.execute(text("SELECT 1"))
#         logger.info("PostgreSQL连接成功")
#     except Exception:
#         logger.exception("PostgreSQL连接失败")
#         raise
#     yield
#     await engine.dispose()


app = FastAPI(title="UV + FastAPI Demo", lifespan=lifespan)

app.include_router(run_router)
