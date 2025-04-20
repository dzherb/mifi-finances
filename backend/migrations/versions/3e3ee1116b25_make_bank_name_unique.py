"""make bank name unique

Revision ID: 3e3ee1116b25
Revises: 53dd2e9dcc84
Create Date: 2025-04-20 13:17:33.525881

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3e3ee1116b25'
down_revision: Union[str, None] = '53dd2e9dcc84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(op.f('uq_banks_name'), 'banks', ['name'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_banks_name'), 'banks', type_='unique')
