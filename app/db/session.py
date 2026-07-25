from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings
from app.db.url import database_connect_args, database_url_for_engine

engine = create_async_engine(
    database_url_for_engine(settings.async_database_url),
    pool_pre_ping=True,
    connect_args=database_connect_args(settings.async_database_url),
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """请求级数据库会话，供 FastAPI Depends 注入。"""
    async with AsyncSessionLocal() as session:
        yield session
