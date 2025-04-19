"""add transation related tables

Revision ID: 7064086b6a48
Revises: 2743d04ad79a
Create Date: 2025-04-19 13:43:56.605192

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '7064086b6a48'
down_revision: Union[str, None] = '2743d04ad79a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sa.Enum(
        'NEW',
        'CONFIRMED',
        'PROCESSING',
        'CANCELLED',
        'EXECUTED',
        'DELETED',
        'REFUNDED',
        name='transactionstatus',
    ).create(op.get_bind())
    sa.Enum('CREDIT', 'DEBIT', name='transactiontype').create(op.get_bind())
    sa.Enum('INDIVIDUAL', 'LEGAL_ENTITY', name='partytype').create(
        op.get_bind(),
    )
    op.create_table(
        'banks',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'transaction_categories',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'transactions',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'party_type',
            postgresql.ENUM(
                'INDIVIDUAL',
                'LEGAL_ENTITY',
                name='partytype',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'transaction_type',
            postgresql.ENUM(
                'CREDIT',
                'DEBIT',
                name='transactiontype',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            'comment',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column('amount', sa.Numeric(precision=12, scale=5), nullable=False),
        sa.Column(
            'status',
            postgresql.ENUM(
                'NEW',
                'CONFIRMED',
                'PROCESSING',
                'CANCELLED',
                'EXECUTED',
                'DELETED',
                'REFUNDED',
                name='transactionstatus',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('sender_bank_id', sa.Integer(), nullable=False),
        sa.Column(
            'account_number',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column('recipient_bank_id', sa.Integer(), nullable=False),
        sa.Column(
            'recipient_inn',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column(
            'recipient_account_number',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column(
            'recipient_phone',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['category_id'],
            ['transaction_categories.id'],
        ),
        sa.ForeignKeyConstraint(['recipient_bank_id'], ['banks.id']),
        sa.ForeignKeyConstraint(['sender_bank_id'], ['banks.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('transactions')
    op.drop_table('transaction_categories')
    op.drop_table('banks')
    sa.Enum('INDIVIDUAL', 'LEGAL_ENTITY', name='partytype').drop(op.get_bind())
    sa.Enum('CREDIT', 'DEBIT', name='transactiontype').drop(op.get_bind())
    sa.Enum(
        'NEW',
        'CONFIRMED',
        'PROCESSING',
        'CANCELLED',
        'EXECUTED',
        'DELETED',
        'REFUNDED',
        name='transactionstatus',
    ).drop(op.get_bind())
