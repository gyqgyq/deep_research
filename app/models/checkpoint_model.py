"""Run 恢复点 ORM 模型。"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Checkpoints(Base):
    """恢复点，不是事件日志（表 checkpoints）。"""

    __tablename__ = "checkpoints"
    __table_args__ = (
        UniqueConstraint("run_id", "checkpoint_index", name="uq_checkpoints_run_index"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("agent_runs.id"),
        nullable=False,
    )
    # 第几次保存恢复点
    checkpoint_index: Mapped[int] = mapped_column(Integer, nullable=False)
    # 下一次恢复时需要的最小状态
    state_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
