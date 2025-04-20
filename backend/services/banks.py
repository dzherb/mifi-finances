from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy.exc import DataError, IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank

BANK_NAME_NOT_UNIQUE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Bank name is not unique',
)


async def get_bank(session: AsyncSession, bank_id: int) -> Bank:
    try:
        bank = await session.get(Bank, bank_id)
    except DataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from e
    if bank is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bank not found',
        )

    return bank


async def all_banks(
    session: AsyncSession,
) -> Sequence[Bank]:
    return (await session.exec(select(Bank))).all()


async def create_bank(session: AsyncSession, name: str) -> Bank:
    bank = Bank(name=name)
    Bank.model_validate(bank)
    try:
        session.add(bank)
        await session.commit()
    except IntegrityError as e:
        raise BANK_NAME_NOT_UNIQUE_EXCEPTION from e
    except DataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from e

    return bank


async def update_bank(session: AsyncSession, bank: Bank) -> Bank:
    try:
        session.add(bank)
        await session.commit()
    except IntegrityError as e:
        raise BANK_NAME_NOT_UNIQUE_EXCEPTION from e
    except DataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from e
    return bank


async def delete_bank(session: AsyncSession, bank_id: int) -> None:
    bank = await get_bank(session, bank_id)
    try:
        await session.delete(bank)
        await session.commit()
    except DataError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        ) from e
