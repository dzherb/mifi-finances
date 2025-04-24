from datetime import datetime
from decimal import Decimal
import enum
import typing

from sqlalchemy import DateTime, VARCHAR
from sqlmodel import Field, Relationship

from core.validators import INN, PhoneNumber
from models.base import BaseModel
from models.mixins import SimpleIdMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from models.bank import Bank
    from models.user import User


class PartyType(str, enum.Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    LEGAL_ENTITY = 'LEGAL_ENTITY'


class TransactionType(str, enum.Enum):
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'


class TransactionStatus(str, enum.Enum):
    NEW = 'NEW'
    CONFIRMED = 'CONFIRMED'
    PROCESSING = 'PROCESSING'
    CANCELLED = 'CANCELLED'
    EXECUTED = 'EXECUTED'
    DELETED = 'DELETED'
    REFUNDED = 'REFUNDED'


class TransactionCategoryBase(BaseModel):
    name: str = Field(unique=True)


class TransactionCategory(
    TransactionCategoryBase,
    TimestampMixin,
    SimpleIdMixin,
    table=True,
):
    __tablename__ = 'transaction_categories'

    transactions: list['Transaction'] = Relationship(back_populates='category')


class TransactionBase(BaseModel):
    party_type: PartyType
    occurred_at: datetime = Field(
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        nullable=False,
    )
    transaction_type: TransactionType
    comment: str = Field(default='')
    amount: Decimal = Field(
        max_digits=12,
        decimal_places=5,
    )
    status: TransactionStatus = Field(default=TransactionStatus.NEW)
    sender_bank_id: int = Field(foreign_key='banks.id')
    account_number: str
    recipient_bank_id: int = Field(foreign_key='banks.id')
    recipient_inn: INN
    recipient_account_number: str
    category_id: int = Field(foreign_key='transaction_categories.id')
    recipient_phone: PhoneNumber = Field(sa_type=VARCHAR)


class Transaction(
    TransactionBase,
    TimestampMixin,
    SimpleIdMixin,
    table=True,
):
    __tablename__ = 'transactions'

    user_id: int = Field(foreign_key='users.id')
    user: 'User' = Relationship(back_populates='transactions')

    sender_bank: 'Bank' = Relationship(
        back_populates='sent_transactions',
        sa_relationship_kwargs={'foreign_keys': 'Transaction.sender_bank_id'},
    )

    recipient_bank: 'Bank' = Relationship(
        back_populates='received_transactions',
        sa_relationship_kwargs={
            'foreign_keys': 'Transaction.recipient_bank_id',
        },
    )

    category: TransactionCategory = Relationship(back_populates='transactions')
