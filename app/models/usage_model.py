"""用量记录 ORM 模型。"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UsageRecords(Base):
    """账单、预算、限流与成本告警用的用量记录（表 usage_records）。"""

    __tablename__ = "usage_records"
    __table_args__ = (
        # 组织维度成本统计
        Index("idx_usage_records_org_created", "org_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    run_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("agent_runs.id"),
        nullable=False,
    )
    org_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        server_default="0",
        nullable=True,
    )
    completion_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        server_default="0",
        nullable=True,
    )
    total_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        server_default="0",
        nullable=True,
    )
    estimated_cost_cents: Mapped[Optional[int]] = mapped_column(
        Integer,
        server_default="0",
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
