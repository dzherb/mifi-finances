"""make transaction category name unique

Revision ID: 939d2c4e88e8
Revises: 3e3ee1116b25
Create Date: 2025-04-20 18:43:09.593478

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '939d2c4e88e8'
down_revision: Union[str, None] = '3e3ee1116b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        op.f('uq_transaction_categories_name'),
        'transaction_categories',
        ['name'],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f('uq_transaction_categories_name'),
        'transaction_categories',
        type_='unique',
    )
