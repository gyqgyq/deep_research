"""AgentRuns 数据访问层（方法体由业务侧自行实现）。"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AgentRuns


class RunRepository:
    """agent_runs 表访问。Service 仅通过本类访问数据库。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, run: AgentRuns) -> AgentRuns:
        """插入一条 run，并 flush 以拿到数据库默认值。"""
        raise NotImplementedError

    async def get_by_id(self, org_id: str, run_id: str) -> AgentRuns | None:
        """按租户 + run_id 查询。"""
        raise NotImplementedError

    async def get_by_idempotency_key(
        self,
        org_id: str,
        idempotency_key: str,
    ) -> AgentRuns | None:
        """按租户 + 幂等键查询（用于创建去重）。"""
        raise NotImplementedError
