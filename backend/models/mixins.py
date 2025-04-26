from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class SimpleIdMixin(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        sa_column_kwargs={'server_default': func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  # type: ignore[call-overload]
        nullable=True,
    )
