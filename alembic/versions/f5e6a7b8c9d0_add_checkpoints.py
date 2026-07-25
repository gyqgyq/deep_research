"""add_checkpoints

Revision ID: f5e6a7b8c9d0
Revises: e4d5f6a7b8c9
Create Date: 2026-07-26 01:54:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f5e6a7b8c9d0"
down_revision: Union[str, Sequence[str], None] = "e4d5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建 checkpoints 表。"""
    op.create_table(
        "checkpoints",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("checkpoint_index", sa.Integer(), nullable=False),
        sa.Column("state_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["run_id"], ["agent_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("run_id", "checkpoint_index", name="uq_checkpoints_run_index"),
    )


def downgrade() -> None:
    """删除 checkpoints 表。"""
    op.drop_table("checkpoints")
