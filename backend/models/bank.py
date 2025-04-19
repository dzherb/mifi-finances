import typing

from sqlmodel import Relationship

from models.base import BaseModel
from models.mixins import SimpleIdMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from models.transaction import Transaction


class Bank(
    BaseModel,
    SimpleIdMixin,
    TimestampMixin,
    table=True,
):
    __tablename__ = 'banks'

    name: str
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
