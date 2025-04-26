from collections.abc import Sequence

from fastapi import APIRouter, status

from api.params import EntityID
from api.responses import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from dependencies.db import Session
from dependencies.users import admin_token_dependency
from models.bank import Bank
from schemas.banks import BankCreate, BankOut, BankOutShort, BankUpdate
from services.banks import BankCRUD

router = APIRouter()


@router.post(
    path='',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST,
    status_code=status.HTTP_201_CREATED,
    response_model=BankOut,
    dependencies=(admin_token_dependency,),
)
async def create_bank(
    session: Session,
    bank: BankCreate,
) -> Bank:
    return await BankCRUD(session).create(Bank.model_validate(bank))


@router.patch(
    path='/{bank_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    response_model=BankOut,
    dependencies=(admin_token_dependency,),
)
async def update_bank(
    session: Session,
    bank: BankUpdate,
    bank_id: EntityID,
) -> Bank:
    crud = BankCRUD(session)
    bank_from_db = await crud.get(bank_id)
    bank_from_db.sqlmodel_update(
        bank.model_dump(exclude_unset=True, exclude_defaults=True),
    )
    return await crud.update(bank_from_db)


@router.delete(
    path='/{bank_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=(admin_token_dependency,),
)
async def delete_bank(
    session: Session,
    bank_id: EntityID,
) -> None:
    await BankCRUD(session).delete(bank_id)


@router.get(
    path='',
    responses=UNAUTHORIZED | FORBIDDEN,
    response_model=list[BankOutShort],
)
async def all_banks(session: Session) -> Sequence[Bank]:
    return await BankCRUD(session).list()
