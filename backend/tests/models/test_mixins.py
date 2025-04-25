from datetime import datetime, timezone

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.mixins import TimestampMixin
from models.transaction import TransactionCategory


@pytest.fixture
async def timestamp_instance(session: AsyncSession) -> TimestampMixin:
    instance = TransactionCategory(name='Test')
    session.add(instance)
    await session.commit()
    return instance


@pytest.mark.xfail(reason='updated_at is currently not working properly')
async def test_updated_at_field(
    session: AsyncSession,
    timestamp_instance: TimestampMixin,
) -> None:
    assert timestamp_instance.updated_at is None

    # update some field
    timestamp_instance.created_at = datetime.now(timezone.utc)
    session.add(timestamp_instance)
    await session.commit()
    await session.refresh(timestamp_instance)

    assert timestamp_instance.updated_at is not None
    last_updated_at = timestamp_instance.updated_at

    # # update again
    timestamp_instance.created_at = datetime.now(timezone.utc)
    session.add(timestamp_instance)
    await session.commit()
    await session.refresh(timestamp_instance)

    assert timestamp_instance.updated_at is not None
    assert timestamp_instance.updated_at != last_updated_at
