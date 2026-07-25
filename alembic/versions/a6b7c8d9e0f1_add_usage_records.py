"""add_usage_records

Revision ID: a6b7c8d9e0f1
Revises: f5e6a7b8c9d0
Create Date: 2026-07-26 01:57:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a6b7c8d9e0f1"
down_revision: Union[str, Sequence[str], None] = "f5e6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建 usage_records 表。"""
    op.create_table(
        "usage_records",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("org_id", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("model", sa.Text(), nullable=True),
        sa.Column("prompt_tokens", sa.Integer(), server_default="0", nullable=True),
        sa.Column("completion_tokens", sa.Integer(), server_default="0", nullable=True),
        sa.Column("total_tokens", sa.Integer(), server_default="0", nullable=True),
        sa.Column("estimated_cost_cents", sa.Integer(), server_default="0", nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """删除 usage_records 表。"""
    op.drop_table("usage_records")
