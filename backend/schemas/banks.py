from pydantic import BaseModel

from models.bank import BankBase
from models.mixins import SimpleIdMixin, TimestampMixin


class BankCreate(BankBase):
    pass


class BankUpdate(BaseModel):
    name: str | None = None


class BankOutShort(BankBase, SimpleIdMixin):
    id: int


class BankOut(BankOutShort, TimestampMixin, SimpleIdMixin):
    pass
