from typing import override

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from models.bank import Bank
from services.crud import BaseCRUD

BANK_NAME_NOT_UNIQUE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Bank name is not unique',
)


class BankCRUD(BaseCRUD[Bank]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = Bank

    @override
    async def create(self, instance: Bank) -> Bank:
        try:
            return await super().create(instance)
        except IntegrityError as e:
            raise BANK_NAME_NOT_UNIQUE_EXCEPTION from e

    @override
    async def update(self, instance: Bank) -> Bank:
        try:
            return await super().update(instance)
        except IntegrityError as e:
            raise BANK_NAME_NOT_UNIQUE_EXCEPTION from e
