from datetime import datetime
from decimal import Decimal

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
from sqlmodel import Field

from core.validators import INN, PhoneNumber
from models.transaction import (
    PartyType,
    Transaction,
    TransactionBase,
    TransactionCategoryBase,
    TransactionStatus,
    TransactionType,
)


class TransactionCategoryCreate(TransactionCategoryBase):
    pass


class TransactionCategoryUpdate(BaseModel):
    name: str | None = None


class TransactionCategoryOutShort(TransactionCategoryBase):
    id: int


class TransactionCategoryOut(
    TransactionCategoryOutShort,
):
    created_at: datetime
    updated_at: datetime | None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    party_type: PartyType | None = None
    occurred_at: datetime | None = None
    transaction_type: TransactionType | None = None
    comment: str | None = None
    amount: Decimal | None = Field(
        default=None,
        max_digits=12,
        decimal_places=5,
    )
    status: TransactionStatus | None = None
    sender_bank_id: int | None = None
    account_number: str | None = None
    recipient_bank_id: int | None = None
    recipient_inn: INN | None = None
    recipient_account_number: str | None = None
    category_id: int | None = None
    recipient_phone: PhoneNumber | None = None


class TransactionOutShort(TransactionBase):
    id: int
    user_id: int


class TransactionOut(TransactionOutShort):
    created_at: datetime
    updated_at: datetime | None


class TransactionFilters(Filter):
    created_at: datetime | None = None
    created_at__gt: datetime | None = None
    created_at__lt: datetime | None = None

    updated_at: datetime | None = None
    updated_at__gt: datetime | None = None
    updated_at__lt: datetime | None = None

    occurred_at: datetime | None = None
    occurred_at__gt: datetime | None = None
    occurred_at__lt: datetime | None = None

    status: TransactionStatus | None = None

    account_number: str | None = None
    account_number__like: str | None = None

    recipient_inn: INN | None = None
    recipient_inn__like: str | None = None

    amount__gt: Decimal | None = None
    amount__lt: Decimal | None = None

    class Constants(Filter.Constants):
        model = Transaction
