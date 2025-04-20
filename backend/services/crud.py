from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy.exc import DataError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.base import BaseModel


class BaseCRUD[T: BaseModel]:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, instance_id: int) -> T:
        try:
            instance = await self.session.get(self.model, instance_id)
        except DataError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return instance

    async def all(
        self,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[T]:
        query = select(self.model).offset(offset).limit(limit)
        return (await self.session.exec(query)).all()

    async def create(self, instance: T) -> T:
        try:
            self.session.add(instance)
            await self.session.commit()
        except DataError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e

        return instance

    async def update(self, instance: T) -> T:
        try:
            self.session.add(instance)
            await self.session.commit()
        except DataError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e
        return instance

    async def delete(self, instance_id: int) -> None:
        instance = await self.get(instance_id)
        try:
            await self.session.delete(instance)
            await self.session.commit()
        except DataError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e
