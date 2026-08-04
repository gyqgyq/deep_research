"""审计日志 ORM 模型。"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLogs(Base):
    """高风险动作审计日志（表 audit_logs）。"""

    __tablename__ = "audit_logs"
    __table_args__ = (
        # 审计日志按组织和时间检索
        Index("idx_audit_logs_org_created", "org_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    org_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(Text, nullable=False)
    run_id: Mapped[Optional[str]] = mapped_column(
        Text,
        ForeignKey("agent_runs.id"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_id: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
