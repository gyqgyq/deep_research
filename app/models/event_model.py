"""Run 事件日志 ORM 模型。"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RunEvents(Base):
    """追加式事件日志，记录 run 发生过什么（表 run_events）。"""

    __tablename__ = "run_events"
    __table_args__ = (
        # 唯一约束本身已带 (run_id, sequence) 索引，等价于事件流按 sequence 读取
        UniqueConstraint("run_id", "sequence", name="uq_run_events_run_sequence"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("agent_runs.id"),
        nullable=False,
    )
    # 保证同一 run 内事件顺序稳定
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
