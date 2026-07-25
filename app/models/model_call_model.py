"""模型调用记录 ORM 模型。"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ModelCalls(Base):
    """每一次模型请求的落库记录（表 model_calls）。"""

    __tablename__ = "model_calls"

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
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    model: Mapped[str] = mapped_column(Text, nullable=False)
    # 原始请求与响应摘要，便于回放
    request_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    response_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    # token 用于成本统计
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    error_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
