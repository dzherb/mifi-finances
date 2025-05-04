import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank
from models.transaction import (
    TransactionCategory,
)
from models.user import User
from services.users import create_user


@pytest.fixture
async def bank(session: AsyncSession) -> Bank:
    bank = Bank(name='Bank')
    session.add(bank)
    await session.commit()
    return bank


@pytest.fixture
async def category(session: AsyncSession) -> TransactionCategory:
    category = TransactionCategory(name='Category')
    session.add(category)
    await session.commit()
    return category


@pytest.fixture
async def another_user(session: AsyncSession) -> User:
    return await create_user(
        session,
        username='user2',
        password='password',
    )
