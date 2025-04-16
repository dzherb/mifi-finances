from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.exc import DataError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    oauth2_scheme,
    TokenData,
    verify_password,
)
from dependencies import get_session
from models.user import User
from schemas.auth import AccessToken, RefreshToken, TokenPair

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
)

AUTH_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect username or password',
)


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> User:
    try:
        result = await session.exec(
            select(User).where(User.username == username),
        )
    except DataError as e:
        raise AUTH_EXCEPTION from e

    user = result.one_or_none()
    if not user or not verify_password(password, user.password):
        raise AUTH_EXCEPTION

    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        token_data = AccessToken(**decode_token(token))
    except (InvalidTokenError, ValidationError) as e:
        raise CREDENTIALS_EXCEPTION from e

    user = await session.get(User, int(token_data.sub))
    if user is None:
        raise CREDENTIALS_EXCEPTION

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions',
            )

    return user


async def get_user_from_refresh_token(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        token_data = RefreshToken(**decode_token(token))
    except (InvalidTokenError, ValidationError) as e:
        raise CREDENTIALS_EXCEPTION from e

    user = await session.get(User, int(token_data.sub))
    if user is None:
        raise CREDENTIALS_EXCEPTION

    if (
        user.last_refresh is None
        or user.last_refresh.timestamp() > token_data.iat
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is expired',
        )

    return user


async def login_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> TokenPair:
    user = await authenticate_user(session, username, password)

    scopes = []
    if user.is_admin:
        scopes.append('admin')

    payload: TokenData = {'sub': str(user.id)}
    return TokenPair(
        access_token=create_access_token(payload, scopes=scopes),
        refresh_token=create_refresh_token(payload),
    )
