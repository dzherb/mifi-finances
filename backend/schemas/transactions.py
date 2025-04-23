from datetime import datetime

from pydantic import BaseModel

from models.transaction import TransactionBase, TransactionCategoryBase


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


class TransactionUpdate(TransactionCreate):
    pass


class TransactionOutShort(TransactionBase):
    id: int


class TransactionOut(TransactionOutShort):
    created_at: datetime
    updated_at: datetime | None
