from collections.abc import Sequence
from typing import Annotated, Final

from fastapi import APIRouter, status
from fastapi.params import Depends, Query
from fastapi_filter import FilterDepends

from api.params import EntityID
from api.responses import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from dependencies.db import Session
from dependencies.params import (
    order_by_dependency,
    OrderByItem,
)
from dependencies.users import AdminUser, CurrentUser
from models.transaction import Transaction, TransactionCategory
from schemas.common import SequenceResponse
from schemas.transactions import (
    TransactionCategoryCreate,
    TransactionCategoryOut,
    TransactionCategoryOutShort,
    TransactionCategoryUpdate,
    TransactionCreate,
    TransactionFilters,
    TransactionOut,
    TransactionUpdate,
)
from services.transactions import (
    TransactionCategoryService,
    TransactionService,
)

router = APIRouter()


TRANSACTIONS_ORDER_BY_FIELDS: Final = (
    'occurred_at',
    'created_at',
    'updated_at',
    'transaction_type',
    'amount',
    'status',
    'recipient_inn',
    'recipient_account_number',
    'recipient_phone',
)

_OrderBy = Depends(
    order_by_dependency(
        fields=TRANSACTIONS_ORDER_BY_FIELDS,
        default=('-occurred_at',),
    ),
)


@router.get(
    path='',
    responses=UNAUTHORIZED | BAD_REQUEST,
    response_model=SequenceResponse[TransactionOut],
)
async def my_transactions(  # noqa: PLR0913
    user: CurrentUser,
    session: Session,
    order_by: Annotated[list[OrderByItem], _OrderBy],
    filters: Annotated[TransactionFilters, FilterDepends(TransactionFilters)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, lt=100)] = 10,
) -> SequenceResponse[Transaction]:
    return await TransactionService(session, user).user_transactions(
        order_by=order_by,
        filters=filters,
        offset=offset,
        limit=limit,
    )


@router.post(
    path='',
    responses=UNAUTHORIZED | BAD_REQUEST,
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def create_transaction(
    user: CurrentUser,
    session: Session,
    transaction: TransactionCreate,
) -> Transaction:
    return await TransactionService(session, user).create_transaction(
        transaction,
    )


@router.patch(
    path='/{transaction_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    response_model=TransactionOut,
)
async def update_transaction(
    user: CurrentUser,
    session: Session,
    transaction_id: EntityID,
    transaction: TransactionUpdate,
) -> Transaction:
    return await TransactionService(session, user).update_transaction(
        transaction_id,
        transaction,
    )


@router.post(
    path='/categories',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST,
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionCategoryOut,
)
async def create_category(
    _: AdminUser,
    session: Session,
    category: TransactionCategoryCreate,
) -> TransactionCategory:
    return await TransactionCategoryService(session).create(
        TransactionCategory.model_validate(category),
    )


@router.patch(
    path='/categories/{category_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    response_model=TransactionCategoryOut,
)
async def update_category(
    _: AdminUser,
    session: Session,
    category: TransactionCategoryUpdate,
    category_id: EntityID,
) -> TransactionCategory:
    crud = TransactionCategoryService(session)
    category_from_db = await crud.get(category_id)
    category_from_db.sqlmodel_update(
        category.model_dump(exclude_unset=True, exclude_defaults=True),
    )
    return await crud.update(category_from_db)


@router.delete(
    path='/categories/{category_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    _: AdminUser,
    session: Session,
    category_id: EntityID,
) -> None:
    await TransactionCategoryService(session).delete(category_id)


@router.get(
    path='/categories',
    responses=UNAUTHORIZED | FORBIDDEN,
    response_model=list[TransactionCategoryOutShort],
)
async def all_categories(session: Session) -> Sequence[TransactionCategory]:
    return await TransactionCategoryService(session).list()
