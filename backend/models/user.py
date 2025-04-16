from datetime import datetime

from sqlmodel import Field

from models.base import Base


class User(Base, table=True):
    __tablename__ = 'users'

    username: str = Field(unique=True)
    password: str

    last_refresh: datetime | None = None
    is_admin: bool = False
