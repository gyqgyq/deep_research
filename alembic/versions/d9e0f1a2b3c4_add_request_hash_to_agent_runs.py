"""add_request_hash_to_agent_runs

Revision ID: d9e0f1a2b3c4
Revises: c8d9e0f1a2b3
Create Date: 2026-08-03 21:58:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d9e0f1a2b3c4"
down_revision: Union[str, Sequence[str], None] = "c8d9e0f1a2b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """为 agent_runs 增加 request_hash。"""
    op.add_column(
        "agent_runs",
        sa.Column("request_hash", sa.Text(), nullable=False, server_default=""),
    )
    op.alter_column("agent_runs", "request_hash", server_default=None)


def downgrade() -> None:
    """移除 agent_runs.request_hash。"""
    op.drop_column("agent_runs", "request_hash")
