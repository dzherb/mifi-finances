"""add time fields

Revision ID: 2743d04ad79a
Revises: d7d496600d53
Create Date: 2025-04-16 19:51:12.078460

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2743d04ad79a'
down_revision: Union[str, None] = 'd7d496600d53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )
    op.add_column(
        'users',
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.alter_column(
        'users',
        'last_refresh',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users',
        'last_refresh',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
