from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from api.responses import UNAUTHORIZED
from dependencies.db import Session
from schemas.auth import LoginRequest, TokenPair, TokenRefresh
from services.auth import login_user, refresh_tokens

router = APIRouter()


@router.post('/login', responses=UNAUTHORIZED)  # type: ignore
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session,
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


@router.post(
    path='/refresh',
    responses=UNAUTHORIZED,  #  type: ignore
)
async def refresh(
    session: Session,
    refresh_token: TokenRefresh,
) -> TokenPair:
    return await refresh_tokens(session, refresh_token.refresh_token)
