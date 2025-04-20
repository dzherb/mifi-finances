import typing

from sqlmodel import Field, Relationship

from models.base import BaseModel
from models.mixins import SimpleIdMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from models.transaction import Transaction


class BankBase(BaseModel):
    name: str = Field(unique=True)


class Bank(
    BankBase,
    TimestampMixin,
    SimpleIdMixin,
    table=True,
):
    __tablename__ = 'banks'

    sent_transactions: list['Transaction'] = Relationship(
        back_populates='sender_bank',
        sa_relationship_kwargs={'foreign_keys': 'Transaction.sender_bank_id'},
    )
    received_transactions: list['Transaction'] = Relationship(
        back_populates='recipient_bank',
        sa_relationship_kwargs={
            'foreign_keys': 'Transaction.recipient_bank_id',
        },
    )
