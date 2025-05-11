from collections.abc import Mapping, Sequence, Set
import typing
from typing import override

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies.params import OrderByItem
from models.transaction import (
    Transaction,
    TransactionCategory,
    TransactionStatus,
)
from models.user import User
from schemas.common import SequenceResponse
from schemas.transactions import TransactionCreate, TransactionUpdate
from services.crud import BaseCRUD, Filters, merge_filters

CATEGORY_NAME_NOT_UNIQUE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Category name is not unique',
)


class TransactionCategoryService(BaseCRUD[TransactionCategory]):
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


class TransactionCRUD(BaseCRUD[Transaction]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = Transaction

    @override
    async def create(self, instance: Transaction) -> Transaction:
        try:
            return await super().create(instance)
        except IntegrityError as e:
            self._handle_integrity_error(e)

    @override
    async def update(self, instance: Transaction) -> Transaction:
        try:
            return await super().update(instance)
        except IntegrityError as e:
            self._handle_integrity_error(e)

    @staticmethod
    def _handle_integrity_error(error: IntegrityError) -> typing.NoReturn:
        if not error.orig:
            raise error

        reason: str = error.orig.args[0]
        related_entity: str

        if 'category_id' in reason:
            related_entity = 'category'
        elif 'sender_bank_id' in reason or 'recipient_bank_id' in reason:
            related_entity = 'bank'
        else:
            raise error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{related_entity} does not exist',
        ) from error


class TransactionGuard:
    EDIT_FORBIDDEN_STATUSES: typing.ClassVar[Set[TransactionStatus]] = {
        TransactionStatus.CONFIRMED,
        TransactionStatus.PROCESSING,
        TransactionStatus.CANCELLED,
        TransactionStatus.EXECUTED,
        TransactionStatus.REFUNDED,
    }

    DELETE_FORBIDDEN_STATUSES: typing.ClassVar[Set[TransactionStatus]] = {
        TransactionStatus.CONFIRMED,
        TransactionStatus.PROCESSING,
        TransactionStatus.CANCELLED,
        TransactionStatus.EXECUTED,
        TransactionStatus.REFUNDED,
    }

    ALLOWED_UPDATE_FIELDS: typing.ClassVar[Set[str]] = {
        'party_type',
        'occurred_at',
        'comment',
        'amount',
        'status',
        'sender_bank_id',
        'recipient_bank_id',
        'recipient_inn',
        'category_id',
        'recipient_phone',
    }

    def __init__(self, transaction: Transaction, user: User) -> None:
        self.transaction = transaction
        self.user = user

    def ensure_editable(self, update_data: Mapping[str, typing.Any]) -> None:
        self._ensure_user_is_owner_or_admin()

        if self.transaction.status in self.EDIT_FORBIDDEN_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction with status '{self.transaction.status}' "
                f'cannot be edited',
            )

        for field in update_data:
            if field not in self.ALLOWED_UPDATE_FIELDS:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Field '{field}' is not editable",
                )

    def ensure_deletable(self) -> None:
        self._ensure_user_is_owner_or_admin()

        if self.transaction.status in self.DELETE_FORBIDDEN_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction with status '{self.transaction.status}' "
                f'cannot be deleted',
            )

    def _ensure_user_is_owner_or_admin(self) -> None:
        owner_or_admin = (
            self.user.is_admin or self.user.id == self.transaction.user_id
        )
        if not owner_or_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to perform this operation',
            )


class TransactionService:
    def __init__(self, session: AsyncSession, user: User) -> None:
        self.crud = TransactionCRUD(session)
        self.user = user

    async def create_transaction(
        self,
        transaction: TransactionCreate,
    ) -> Transaction:
        transaction_with_user = Transaction.model_validate(
            transaction,
            update={'user_id': self.user.id},
        )
        return await self.crud.create(transaction_with_user)

    async def update_transaction(
        self,
        transaction_id: int,
        updated_transaction: TransactionUpdate,
    ) -> Transaction:
        current_transaction = await self.crud.get(transaction_id)

        update_data = updated_transaction.model_dump(
            exclude_unset=True,
            exclude_defaults=True,
        )
        TransactionGuard(current_transaction, self.user).ensure_editable(
            update_data,
        )

        current_transaction.sqlmodel_update(update_data)
        return await self.crud.update(current_transaction)

    async def delete_transaction(self, transaction_id: int) -> None:
        transaction = await self.crud.get(transaction_id)

        TransactionGuard(transaction, self.user).ensure_deletable()

        transaction.status = TransactionStatus.DELETED
        await self.crud.update(transaction)

    async def user_transactions(
        self,
        order_by: Sequence[OrderByItem] | None = None,
        filters: Filters | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> SequenceResponse[Transaction]:
        filters = merge_filters(
            (Transaction.user_id == self.user.id,),
            filters,
        )

        count = await self.crud.count(filters=filters)
        items = await self.crud.list(
            filters=filters,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )
        return SequenceResponse(items=items, total_count=count)
