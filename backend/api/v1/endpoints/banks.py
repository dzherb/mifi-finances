from typing import Annotated

from fastapi import APIRouter, Path, status

from api.responses import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from dependencies.db import Session
from dependencies.users import AdminUser
from models.bank import Bank
from schemas.banks import BankCreate, BankOut, BankUpdate
import services.banks as bank_service

router = APIRouter()

BankID = Annotated[int, Path(..., gt=0)]


@router.post(
    path='',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST,
    status_code=status.HTTP_201_CREATED,
    response_model=BankOut,
)
async def create_bank(
    _: AdminUser,
    session: Session,
    bank: BankCreate,
) -> Bank:
    return await bank_service.create_bank(session, bank.name)


@router.patch(
    path='/{bank_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    response_model=BankOut,
)
async def update_bank(
    _: AdminUser,
    session: Session,
    bank: BankUpdate,
    bank_id: BankID,
) -> Bank:
    bank_from_db = await bank_service.get_bank(session, bank_id)
    updated_bank = bank_from_db.model_copy(
        update=bank.model_dump(exclude_unset=True, exclude_none=True),
    )
    return await bank_service.update_bank(session, updated_bank)


@router.delete(
    path='/{bank_id}',
    responses=UNAUTHORIZED | FORBIDDEN | BAD_REQUEST | NOT_FOUND,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bank(
    _: AdminUser,
    session: Session,
    bank_id: BankID,
) -> None:
    await bank_service.delete_bank(session, bank_id)
    return
