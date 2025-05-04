from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import func, Select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql._typing import _ColumnExpressionArgument
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies.params import OrderByItem
from models.base import BaseModel
from services.common import is_data_error

type WhereClause = _ColumnExpressionArgument[bool] | bool


class BaseCRUD[T: BaseModel]:
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count(
        self,
        filters: Sequence[WhereClause] | None = None,
    ) -> int:
        query = select(func.count()).select_from(self.model)
        query = self._apply_filters(query, filters)
        result = await self.session.exec(query)
        return result.one()

    async def get(self, instance_id: int) -> T:
        try:
            instance = await self.session.get(self.model, instance_id)
        except DBAPIError as e:
            if is_data_error(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e

            raise e

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return instance

    async def list(
        self,
        filters: Sequence[WhereClause] | None = None,
        order_by: Sequence[OrderByItem] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[T]:
        query = select(self.model)

        query = self._apply_filters(query, filters)

        if order_by is not None:
            order_by_seq = (
                getattr(self.model, order_column.field).desc()
                if order_column.desc
                else getattr(self.model, order_column.field)
                for order_column in order_by
            )
            query = query.order_by(*order_by_seq)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        try:
            result = await self.session.exec(query)
        except DBAPIError as e:
            if is_data_error(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e

            raise e

        return result.all()

    async def create(self, instance: T) -> T:
        try:
            self.session.add(instance)
            await self.session.commit()
        except DBAPIError as e:
            if is_data_error(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e

            raise e

        return instance

    async def update(self, instance: T) -> T:
        try:
            self.session.add(instance)
            await self.session.commit()
        except DBAPIError as e:
            if is_data_error(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e

            raise e

        return instance

    async def delete(self, instance_id: int) -> None:
        instance = await self.get(instance_id)
        try:
            await self.session.delete(instance)
            await self.session.commit()
        except DBAPIError as e:
            if is_data_error(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                ) from e

            raise e

    def _apply_filters(
        self,
        query: Select[T],
        filters: Sequence[WhereClause] | None = None,
    ) -> Select[T]:
        if filters is not None:
            for condition in filters:
                query = query.where(condition)

        return query
