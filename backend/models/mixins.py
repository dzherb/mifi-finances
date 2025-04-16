from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field


class SimpleIdMixin:
    id: int | None = Field(default=None, primary_key=True)


class TimestampMixin:
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            nullable=True,
        ),
    )
