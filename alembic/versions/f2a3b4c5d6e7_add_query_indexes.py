"""add_query_indexes

Revision ID: f2a3b4c5d6e7
Revises: e1f2a3b4c5d6
Create Date: 2026-08-04 11:17:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2a3b4c5d6e7"
down_revision: Union[str, Sequence[str], None] = "e1f2a3b4c5d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """补充常用查询索引。

    agent_steps / run_events 的 (run_id, step_index|sequence) 已有唯一约束索引，不再重复创建。
    """
    op.create_index(
        "idx_agent_runs_org_created",
        "agent_runs",
        ["org_id", "created_at"],
        unique=False,
        postgresql_ops={"created_at": "DESC"},
    )
    op.create_index(
        "idx_agent_runs_status_created",
        "agent_runs",
        ["status", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_model_calls_run_created",
        "model_calls",
        ["run_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_tool_calls_run_created",
        "tool_calls",
        ["run_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_tool_calls_tool_status",
        "tool_calls",
        ["tool_name", "status", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_usage_records_org_created",
        "usage_records",
        ["org_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "idx_audit_logs_org_created",
        "audit_logs",
        ["org_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """删除本迁移新增的查询索引。"""
    op.drop_index("idx_audit_logs_org_created", table_name="audit_logs")
    op.drop_index("idx_usage_records_org_created", table_name="usage_records")
    op.drop_index("idx_tool_calls_tool_status", table_name="tool_calls")
    op.drop_index("idx_tool_calls_run_created", table_name="tool_calls")
    op.drop_index("idx_model_calls_run_created", table_name="model_calls")
    op.drop_index("idx_agent_runs_status_created", table_name="agent_runs")
    op.drop_index("idx_agent_runs_org_created", table_name="agent_runs")
