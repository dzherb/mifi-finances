from datetime import datetime, timezone
from typing import Any

from fastapi import status
from httpx import AsyncClient
import pytest
from pytest_lazy_fixtures import lf
from sqlmodel import select
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


async def test_transaction_create(
    authenticated_client: AsyncClient,
    session: AsyncSession,
    user: User,
    bank: Bank,
    category: TransactionCategory,
) -> None:
    create_data = {
        'party_type': PartyType.INDIVIDUAL.value,
        'status': TransactionStatus.NEW.value,
        'transaction_type': TransactionType.CREDIT.value,
        'amount': 100.0,
        'comment': 'Test',
        'occurred_at': datetime.now(timezone.utc).isoformat(),
        'sender_bank_id': bank.id,
        'account_number': '123456',
        'recipient_bank_id': bank.id,
        'recipient_inn': '6449013711',
        'recipient_account_number': '123456',
        'category_id': category.id,
        'recipient_phone': '+79999999999',
    }
    response = await authenticated_client.post(
        url='/api/v1/transactions',
        json=create_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    query = select(Transaction).where(Transaction.id == response_data['id'])
    transaction_from_db = (await session.exec(query)).one_or_none()

    assert transaction_from_db is not None
    assert transaction_from_db.user_id == user.id


@pytest.mark.parametrize(
    'update_data',
    [
        {'category_id': lf('another_category.id')},
        {'recipient_bank_id': lf('another_bank.id')},
        {'recipient_phone': '+79991231212'},
        {'comment': 'new comment', 'amount': 42.0},
        {},
    ],
)
async def test_transaction_update_success(
    authenticated_client: AsyncClient,
    session: AsyncSession,
    transaction: Transaction,
    update_data: dict[str, Any],
) -> None:
    original_transaction = transaction.model_copy()

    response = await authenticated_client.patch(
        url=f'/api/v1/transactions/{transaction.id}',
        json=update_data,
    )
    assert response.status_code == status.HTTP_200_OK

    await session.refresh(transaction)

    # assert that the desired fields are updated
    for field in update_data:
        assert getattr(transaction, field) != getattr(
            original_transaction,
            field,
        )

    # assert that we didn't update other fields
    for field in original_transaction.model_dump():
        if field in update_data or field == 'updated_at':
            continue

        assert getattr(transaction, field) == getattr(
            original_transaction,
            field,
        )
