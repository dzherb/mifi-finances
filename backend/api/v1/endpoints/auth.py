from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from api.responses import UNAUTHORIZED
from dependencies import get_session
from schemas.auth import LoginRequest, TokenPair
from services.auth import login_user

router = APIRouter()


@router.post('/login', responses=UNAUTHORIZED)  # type: ignore
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TokenPair:
    try:
        login_data = LoginRequest(
            username=form_data.username,
            password=form_data.password,
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from e

    return await login_user(
        username=login_data.username,
        password=login_data.password,
        session=session,
    )
