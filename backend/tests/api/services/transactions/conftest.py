from datetime import datetime, timezone

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


@pytest.fixture
async def bank(session: AsyncSession) -> Bank:
    bank = Bank(name='Bank1')
    session.add(bank)
    await session.commit()
    return bank


@pytest.fixture
async def category(session: AsyncSession) -> TransactionCategory:
    category = TransactionCategory(name='Category1')
    session.add(category)
    await session.commit()
    return category


@pytest.fixture
async def transaction(
    session: AsyncSession,
    bank: Bank,
    category: TransactionCategory,
    user: User,
) -> Transaction:
    transaction = Transaction(
        user_id=user.id,
        party_type=PartyType.INDIVIDUAL,
        status=TransactionStatus.NEW,
        transaction_type=TransactionType.CREDIT,
        amount=100.0,
        comment='Test',
        occurred_at=datetime.now(timezone.utc),
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
    return transaction
