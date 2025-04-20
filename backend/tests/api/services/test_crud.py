from fastapi import HTTPException, status
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank
from schemas.banks import BankOut
from services.crud import BaseCRUD


@pytest.fixture
async def bank(session: AsyncSession) -> Bank:
    bank = Bank(name='Test Bank')
    session.add(bank)
    await session.commit()
    await session.refresh(bank)
    return bank


@pytest.fixture
def crud(session: AsyncSession) -> BaseCRUD[Bank]:
    class BankCRUD(BaseCRUD[Bank]):
        model = Bank

    return BankCRUD(session)


async def test_get_success(crud: BaseCRUD[Bank], bank: BankOut) -> None:
    result = await crud.get(bank.id)
    assert result.id == bank.id
    assert result.name == bank.name


async def test_get_not_found(crud: BaseCRUD[Bank]) -> None:
    with pytest.raises(HTTPException) as exc_info:
        await crud.get(99999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


async def test_all(crud: BaseCRUD[Bank], bank: BankOut) -> None:
    results = await crud.all()
    assert any(b.id == bank.id for b in results)


async def test_create(crud: BaseCRUD[Bank]) -> None:
    new_bank = Bank(name='New Bank')
    created = await crud.create(new_bank)
    assert created.id is not None
    assert created.name == 'New Bank'


async def test_update(crud: BaseCRUD[Bank], bank: Bank) -> None:
    bank.name = 'Updated'
    updated = await crud.update(bank)
    assert updated.name == 'Updated'


async def test_delete(crud: BaseCRUD[Bank], bank: BankOut) -> None:
    await crud.delete(bank.id)
    with pytest.raises(HTTPException) as exc_info:
        await crud.get(bank.id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
