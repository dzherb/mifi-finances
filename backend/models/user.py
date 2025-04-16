from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field

from models.base import BaseModel
from models.mixins import SimpleIdMixin, TimestampMixin


class User(BaseModel, SimpleIdMixin, TimestampMixin, table=True):
    __tablename__ = 'users'

    username: str = Field(unique=True)
    password: str

    last_refresh: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    is_admin: bool = False
