"""add_created_at_to_agent_steps

Revision ID: e1f2a3b4c5d6
Revises: d9e0f1a2b3c4
Create Date: 2026-08-04 11:11:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1f2a3b4c5d6"
down_revision: Union[str, Sequence[str], None] = "d9e0f1a2b3c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """为 agent_steps 增加 created_at，并将 started_at 改为可空。"""
    op.add_column(
        "agent_steps",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    # 历史数据：创建时间回填为原 started_at
    op.execute(sa.text("UPDATE agent_steps SET created_at = started_at"))
    op.alter_column("agent_steps", "created_at", server_default=sa.text("now()"))
    op.alter_column(
        "agent_steps",
        "started_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None,
    )


def downgrade() -> None:
    """回滚 agent_steps.created_at，并恢复 started_at 为非空。"""
    op.execute(sa.text("UPDATE agent_steps SET started_at = created_at WHERE started_at IS NULL"))
    op.alter_column(
        "agent_steps",
        "started_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("now()"),
    )
    op.drop_column("agent_steps", "created_at")
