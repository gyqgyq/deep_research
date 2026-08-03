"""AgentRuns 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentRuns


class RunRepository:
    """agent_runs 表访问。Service 仅通过本类访问数据库。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, run: AgentRuns) -> AgentRuns:
        """插入一条 run，并 flush 以拿到数据库默认值。"""
        self._session.add(run)
        await self._session.flush()
        await self._session.refresh(run)
        return run

    async def get_run_by_id_and_org(self, run_id: str, org_id: str) -> AgentRuns | None:
        """按 run_id + 租户查询。org_id是租户隔离条件，防止拿别人的run"""
        stmt = select(AgentRuns).where(
            AgentRuns.id == run_id,
            AgentRuns.org_id == org_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_run_by_idempotency_key(
        self,
        org_id: str,
        idempotency_key: str,
    ) -> AgentRuns | None:
        """按租户 + 幂等键查询（用于创建去重）。"""
        stmt = select(AgentRuns).where(
            AgentRuns.org_id == org_id,
            AgentRuns.idempotency_key == idempotency_key,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
