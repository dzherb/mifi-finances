"""add fields to user

Revision ID: d7d496600d53
Revises: 7cf4d35a549b
Create Date: 2025-04-16 01:31:09.913059

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd7d496600d53'
down_revision: Union[str, None] = '7cf4d35a549b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column('last_refresh', sa.DateTime(), nullable=True),
    )
    op.add_column(
        'users',
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'last_refresh')
