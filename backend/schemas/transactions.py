from pydantic import BaseModel

from models.mixins import SimpleIdMixin, TimestampMixin
from models.transaction import TransactionCategoryBase


class TransactionCategoryCreate(TransactionCategoryBase):
    pass


class TransactionCategoryUpdate(BaseModel):
    name: str | None = None


class TransactionCategoryOutShort(TransactionCategoryBase, SimpleIdMixin):
    id: int


class TransactionCategoryOut(
    TransactionCategoryOutShort,
    TimestampMixin,
    SimpleIdMixin,
):
    pass
