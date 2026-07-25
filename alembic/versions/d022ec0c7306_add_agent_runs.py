"""add_agent_runs

Revision ID: d022ec0c7306
Revises:
Create Date: 2026-07-26 00:39:53.954172

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d022ec0c7306"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建 agent_runs"""
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("org_id", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("run_type", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("idempotency_key", sa.Text(), nullable=False),
        sa.Column("input_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("output_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("org_id", "idempotency_key", name="uq_agent_runs_org_idempotency"),
    )

    # 数据库侧在 UPDATE 时自动刷新 updated_at
    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_agent_runs_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_agent_runs_set_updated_at
        BEFORE UPDATE ON agent_runs
        FOR EACH ROW
        EXECUTE PROCEDURE set_agent_runs_updated_at();
        """
    )


def downgrade() -> None:
    """删除 agent_runs 及其 updated_at 触发器。"""
    op.execute("DROP TRIGGER IF EXISTS trg_agent_runs_set_updated_at ON agent_runs;")
    op.execute("DROP FUNCTION IF EXISTS set_agent_runs_updated_at();")
    op.drop_table("agent_runs")
