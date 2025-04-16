"""update user fields

Revision ID: 7cf4d35a549b
Revises: d05c0682f79d
Create Date: 2025-04-15 23:25:00.849590

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '7cf4d35a549b'
down_revision: Union[str, None] = 'd05c0682f79d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'password',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
    )
    op.create_unique_constraint('unique_username', 'users', ['username'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_username', 'users', type_='unique')
    op.drop_column('users', 'password')
