# ruff: noqa: PLR2004
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank
from models.transaction import (
    PartyType,
    Transaction,
    TransactionCategory,
    TransactionStatus,
    TransactionType,
)
from models.user import User
from schemas.analytics import DynamicsByIntervalEntry, Interval
from services.analytics.analytics import DynamicsByIntervalService
from services.users import create_user


@pytest.fixture
async def another_user(session: AsyncSession) -> User:
    return await create_user(
        session,
        username='user2',
        password='password',
    )


async def _create_transaction(
    session: AsyncSession,
    user: User,
    bank: Bank,
    category: TransactionCategory,
    occurred_at: datetime,
) -> None:
    transaction = Transaction(
        user_id=user.id,
        party_type=PartyType.INDIVIDUAL,
        status=TransactionStatus.NEW,
        transaction_type=TransactionType.CREDIT,
        amount=Decimal('100.0'),
        comment='Test',
        occurred_at=occurred_at,
        sender_bank_id=bank.id,
        account_number='123456',
        recipient_bank_id=bank.id,
        recipient_inn='6449013711',
        recipient_account_number='123456',
        category_id=category.id,
        recipient_phone='+79999999999',
    )
    session.add(transaction)
    await session.commit()


@pytest.fixture
async def transactions(
    session: AsyncSession,
    user: User,
    another_user: User,
    bank: Bank,
    category: TransactionCategory,
) -> None:
    transactions = [
        (user, '2024-07-01T10:00:00Z'),
        (user, '2024-07-01T10:00:00Z'),
        (another_user, '2024-07-01T10:00:00Z'),
        (another_user, '2024-07-04T10:00:00Z'),
        (user, '2024-07-05T10:00:00Z'),
        (user, '2024-07-08T10:00:00Z'),
        (user, '2024-07-23T10:00:00Z'),
        (another_user, '2024-07-24T10:00:00Z'),
        (user, '2024-07-24T10:00:00Z'),
        (user, '2024-09-13T10:00:00Z'),
        (user, '2025-02-13T10:00:00Z'),
    ]

    for transaction_user, date in transactions:
        await _create_transaction(
            session,
            user=transaction_user,
            bank=bank,
            category=category,
            occurred_at=datetime.fromisoformat(date),
        )


@pytest.mark.parametrize(
    ('start', 'end_delta', 'interval', 'expected'),
    [
        (
            datetime.fromisoformat('2024-07-01'),
            relativedelta(months=1),
            Interval.WEEK,
            [
                DynamicsByIntervalEntry(date='2024-07-01', count=3),
                DynamicsByIntervalEntry(date='2024-07-08', count=1),
                DynamicsByIntervalEntry(date='2024-07-15', count=0),
                DynamicsByIntervalEntry(date='2024-07-22', count=2),
                DynamicsByIntervalEntry(date='2024-07-29', count=0),
            ],
        ),
        (
            datetime.fromisoformat('2024-07-01'),
            relativedelta(months=2),
            Interval.MONTH,
            [
                DynamicsByIntervalEntry(date='2024-07-01', count=6),
                DynamicsByIntervalEntry(date='2024-08-01', count=0),
                DynamicsByIntervalEntry(date='2024-09-01', count=1),
            ],
        ),
        (
            datetime.fromisoformat('2024-07-01'),
            relativedelta(months=5),
            Interval.QUARTER,
            [
                DynamicsByIntervalEntry(date='2024-07-01', count=7),
                DynamicsByIntervalEntry(date='2024-10-01', count=0),
            ],
        ),
        (
            datetime.fromisoformat('2024-07-01'),
            relativedelta(years=2),
            Interval.YEAR,
            [
                DynamicsByIntervalEntry(date='2024-01-01', count=7),
                DynamicsByIntervalEntry(date='2025-01-01', count=1),
                DynamicsByIntervalEntry(date='2026-01-01', count=0),
            ],
        ),
    ],
)
@pytest.mark.usefixtures('transactions')
async def test_dynamics_by_interval(  # noqa: PLR0913
    session: AsyncSession,
    user: User,
    start: datetime,
    end_delta: relativedelta,
    interval: Interval,
    expected: list[DynamicsByIntervalEntry],
) -> None:
    service = DynamicsByIntervalService(
        session=session,
        user=user,
    )

    result = await service.get(
        start=start,
        end=start + end_delta,
        interval=interval,
    )

    for entry_got, entry_expected in zip(
        result.entries,
        expected,
        strict=True,
    ):
        assert entry_got == entry_expected
