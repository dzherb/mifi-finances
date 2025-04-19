"""add user field to transaction

Revision ID: 53dd2e9dcc84
Revises: 7064086b6a48
Create Date: 2025-04-19 15:05:28.905959

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '53dd2e9dcc84'
down_revision: Union[str, None] = '7064086b6a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'transactions',
        sa.Column('user_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f('fk_transactions_user_id_users'),
        'transactions',
        'users',
        ['user_id'],
        ['id'],
    )
    op.drop_constraint('unique_username', 'users', type_='unique')
    op.create_unique_constraint(
        op.f('uq_users_username'),
        'users',
        ['username'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_users_username'), 'users', type_='unique')
    op.create_unique_constraint('unique_username', 'users', ['username'])
    op.drop_constraint(
        op.f('fk_transactions_user_id_users'),
        'transactions',
        type_='foreignkey',
    )
    op.drop_column('transactions', 'user_id')
