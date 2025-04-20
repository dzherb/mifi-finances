from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from models.transaction import TransactionCategory
from services.crud import BaseCRUD

CATEGORY_NAME_NOT_UNIQUE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Category name is not unique',
)


class TransactionCategoryCRUD(BaseCRUD[TransactionCategory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = TransactionCategory

    async def create(
        self,
        instance: TransactionCategory,
    ) -> TransactionCategory:
        try:
            return await super().create(instance)
        except IntegrityError as e:
            raise CATEGORY_NAME_NOT_UNIQUE_EXCEPTION from e

    async def update(
        self,
        instance: TransactionCategory,
    ) -> TransactionCategory:
        try:
            return await super().update(instance)
        except IntegrityError as e:
            raise CATEGORY_NAME_NOT_UNIQUE_EXCEPTION from e
