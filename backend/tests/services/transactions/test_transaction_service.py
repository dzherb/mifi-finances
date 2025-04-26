from datetime import datetime, timezone
import typing

from fastapi import HTTPException
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
from schemas.transactions import TransactionCreate, TransactionUpdate
from services.transactions import TransactionService


@pytest.fixture
def transaction_to_create(
    user: User,
    bank: Bank,
    category: TransactionCategory,
) -> TransactionCreate:
    return TransactionCreate(
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


async def test_create_transaction(
    session: AsyncSession,
    user: User,
    transaction_to_create: TransactionCreate,
) -> None:
    service = TransactionService(session, user)
    result = await service.create_transaction(transaction_to_create)

    assert result.id is not None
    assert result.user_id == user.id
    assert result.comment == 'Test'


async def test_update_transaction_success(
    session: AsyncSession,
    user: User,
    transaction: Transaction,
) -> None:
    service = TransactionService(session, user)

    update_data = TransactionUpdate(comment='Updated')
    transaction_id = typing.cast(int, transaction.id)
    updated = await service.update_transaction(transaction_id, update_data)

    assert updated.comment == 'Updated'


async def test_update_transaction_forbidden_field(
    session: AsyncSession,
    user: User,
    transaction: Transaction,
) -> None:
    service = TransactionService(session, user)

    transaction.status = TransactionStatus.CONFIRMED
    session.add(transaction)
    await session.commit()

    update_data = TransactionUpdate(comment='Fail')

    transaction_id = typing.cast(int, transaction.id)
    with pytest.raises(HTTPException) as exc_info:
        await service.update_transaction(transaction_id, update_data)

    assert 'cannot be edited' in str(exc_info.value)


async def test_delete_transaction_success(
    session: AsyncSession,
    user: User,
    transaction: Transaction,
) -> None:
    service = TransactionService(session, user)

    assert transaction.id is not None  # for mypy

    await service.delete_transaction(transaction.id)
    updated_transaction = await service.crud.get(transaction.id)

    assert updated_transaction.status == TransactionStatus.DELETED
