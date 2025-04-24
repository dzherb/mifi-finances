from collections.abc import Sequence

from fastapi import APIRouter, status

from api.params import EntityID
from api.responses import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from dependencies.db import Session
from dependencies.users import AdminUser, CurrentUser
from models.transaction import Transaction, TransactionCategory
from schemas.transactions import (
    TransactionCategoryCreate,
    TransactionCategoryOut,
    TransactionCategoryOutShort,
    TransactionCategoryUpdate,
    TransactionCreate,
    TransactionOut,
)
from services.transactions import TransactionCategoryCRUD, TransactionCRUD

router = APIRouter()


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
    new_transaction = Transaction.model_validate(
        transaction,
        update={'user_id': user.id},
    )
    return await TransactionCRUD(session).create(new_transaction)


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
    return await TransactionCategoryCRUD(session).create(
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
    crud = TransactionCategoryCRUD(session)
    category_from_db = await crud.get(category_id)
    updated_category = category_from_db.model_copy(
        update=category.model_dump(exclude_unset=True, exclude_defaults=True),
    )
    return await crud.update(updated_category)


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
    await TransactionCategoryCRUD(session).delete(category_id)


@router.get(
    path='/categories',
    responses=UNAUTHORIZED | FORBIDDEN,
    response_model=list[TransactionCategoryOutShort],
)
async def all_categories(session: Session) -> Sequence[TransactionCategory]:
    return await TransactionCategoryCRUD(session).all()
