from datetime import datetime

from pydantic import BaseModel

from models.transaction import TransactionCategoryBase


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
