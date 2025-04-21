from datetime import datetime

from pydantic import BaseModel

from models.bank import BankBase


class BankCreate(BankBase):
    pass


class BankUpdate(BaseModel):
    name: str | None = None


class BankOutShort(BankBase):
    id: int


class BankOut(BankOutShort):
    created_at: datetime
    updated_at: datetime | None
