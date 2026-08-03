"""Agent 执行主记录 ORM 模型。"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AgentRuns(Base):
    """一次 Agent 执行的主记录（表 agent_runs）。"""

    __tablename__ = "agent_runs"
    __table_args__ = (
        UniqueConstraint("org_id", "idempotency_key", name="uq_agent_runs_org_idempotency"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    # 租户隔离键，查询应始终带上
    org_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    run_type: Mapped[str] = mapped_column(Text, nullable=False)
    # 状态机当前状态，如 queued / running / succeeded
    status: Mapped[str] = mapped_column(Text, nullable=False)
    # 同一组织内业务请求去重键
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    # 请求入参哈希，用于幂等键冲突时区分是否同一请求
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    # 不同 run_type 可用不同结构，先用 JSONB 承载
    input_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    output_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # 更新时由数据库触发器自动刷新
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
