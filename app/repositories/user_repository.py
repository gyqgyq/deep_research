"""用户数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users


class UserRepository:
    """users 表访问。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: Users) -> Users:
        """插入用户并 flush。"""
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        return user

    async def get_by_id(self, user_id: str) -> Users | None:
        """按主键查询。"""
        stmt = select(Users).where(Users.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Users | None:
        """按用户名查询。"""
        stmt = select(Users).where(Users.username == username)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
