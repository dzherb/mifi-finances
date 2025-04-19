from datetime import datetime
import typing

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship

from models.base import BaseModel
from models.mixins import SimpleIdMixin, TimestampMixin

if typing.TYPE_CHECKING:
    from models.transaction import Transaction


class User(BaseModel, SimpleIdMixin, TimestampMixin, table=True):
    __tablename__ = 'users'

    username: str = Field(unique=True)
    password: str

    last_refresh: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    is_admin: bool = False

    transactions: list['Transaction'] = Relationship(back_populates='user')
