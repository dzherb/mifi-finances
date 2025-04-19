from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from api.responses import BAD_REQUEST, UNAUTHORIZED
from dependencies.db import Session
from schemas.auth import LoginRequest, RegisterRequest, TokenPair, TokenRefresh
from services.auth import login_user, refresh_tokens, register_user

router = APIRouter()


@router.post(
    path='/openapi_login',
    responses=UNAUTHORIZED,  # type: ignore
    include_in_schema=False,
)
async def openapi_login(
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
        session=session,
        username=login_data.username,
        password=login_data.password,
        scopes=form_data.scopes,
    )


@router.post('/login', responses=UNAUTHORIZED)  #  type: ignore[arg-type]
async def login(
    login_data: LoginRequest,
    session: Session,
) -> TokenPair:
    return await login_user(
        session=session,
        username=login_data.username,
        password=login_data.password,
    )


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    responses=BAD_REQUEST,  #  type: ignore[arg-type]
)
async def register(
    session: Session,
    register_data: RegisterRequest,
) -> TokenPair:
    return await register_user(
        session=session,
        username=register_data.username,
        password=register_data.password,
    )


@router.post(
    path='/refresh',
    responses=UNAUTHORIZED,  #  type: ignore[arg-type]
)
async def refresh(
    session: Session,
    refresh_token: TokenRefresh,
) -> TokenPair:
    return await refresh_tokens(session, refresh_token.refresh_token)
