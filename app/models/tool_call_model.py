"""工具调用记录 ORM 模型。"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ToolCalls(Base):
    """每一次工具调用的落库记录（表 tool_calls）。"""

    __tablename__ = "tool_calls"
    __table_args__ = (
        UniqueConstraint("tool_name", "idempotency_key", name="uq_tool_calls_name_idempotency"),
        # run 详情页查看工具调用历史
        Index("idx_tool_calls_run_created", "run_id", "created_at"),
        # 按工具名和状态排查失败率
        Index("idx_tool_calls_tool_status", "tool_name", "status", "created_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("agent_runs.id"),
        nullable=False,
    )
    step_id: Mapped[Optional[str]] = mapped_column(
        Text,
        ForeignKey("agent_steps.id"),
        nullable=True,
    )
    tool_name: Mapped[str] = mapped_column(Text, nullable=False)
    args_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    result_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    # 有副作用的工具使用稳定幂等键，防止重复执行
    idempotency_key: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
