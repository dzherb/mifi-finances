from fastapi import HTTPException, status
from fastapi_filter.contrib.sqlalchemy import Filter
import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank
from schemas.banks import BankOut
from services.crud import _apply_filters, BaseCRUD, Filters, merge_filters


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
    results = await crud.list()
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


async def test_count_with_empty_filters(
    crud: BaseCRUD[Bank],
    session: AsyncSession,
) -> None:
    initial_count = await crud.count()

    bank1 = Bank(name='Bank 1')
    bank2 = Bank(name='Bank 2')
    session.add_all([bank1, bank2])
    await session.commit()

    new_count = await crud.count()
    assert new_count == initial_count + 2


async def test_count_with_single_filter(
    crud: BaseCRUD[Bank],
    session: AsyncSession,
) -> None:
    bank = Bank(name='Bank')
    session.add(bank)
    await session.commit()

    count = await crud.count(filters=[Bank.name == 'Bank'])
    assert count == 1


async def test_count_with_no_matches(crud: BaseCRUD[Bank]) -> None:
    count = await crud.count(filters=[Bank.name == 'Not a bank'])
    assert count == 0


class BankFilter(Filter):
    name__like: str | None = None
    id__gte: int | None = None

    class Constants(Filter.Constants):
        model = Bank


@pytest.mark.parametrize(
    ('first', 'second', 'expected'),
    [
        (Bank.id > 1, Bank.name != 'T', [Bank.id > 1, Bank.name != 'T']),  # type: ignore[operator]
        ([Bank.id > 1], Bank.name != 'T', [Bank.id > 1, Bank.name != 'T']),
        (Bank.id > 1, [Bank.name != 'T'], [Bank.id > 1, Bank.name != 'T']),  # type: ignore[operator]
        ([Bank.id > 1], [Bank.name != 'T'], [Bank.id > 1, Bank.name != 'T']),
        (
            BankFilter(name__like='%sb'),
            BankFilter(id__gte=10),
            [BankFilter(name__like='%sb'), BankFilter(id__gte=10)],
        ),
        (
            [BankFilter(name__like='%sb')],
            BankFilter(id__gte=10),
            [BankFilter(name__like='%sb'), BankFilter(id__gte=10)],
        ),
        (
            BankFilter(name__like='%sb'),
            [BankFilter(id__gte=10)],
            [BankFilter(name__like='%sb'), BankFilter(id__gte=10)],
        ),
        (
            [BankFilter(name__like='%sb')],
            [BankFilter(id__gte=10)],
            [BankFilter(name__like='%sb'), BankFilter(id__gte=10)],
        ),
        (
            [BankFilter(name__like='%sb'), Bank.name != 'T'],
            BankFilter(id__gte=10),
            [
                BankFilter(name__like='%sb'),
                Bank.name != 'T',
                BankFilter(id__gte=10),
            ],
        ),
        (
            [BankFilter(name__like='%sb')],
            [Bank.name != 'T', BankFilter(id__gte=10)],
            [
                BankFilter(name__like='%sb'),
                Bank.name != 'T',
                BankFilter(id__gte=10),
            ],
        ),
    ],
)
def test_merge_and_apply_filters(
    first: Filters,
    second: Filters,
    expected: Filters,
) -> None:
    merged_filters = merge_filters(first, second)
    query = _apply_filters(select(Bank), merged_filters)

    query_expected = _apply_filters(select(Bank), expected)
    assert query.compare(query_expected)
