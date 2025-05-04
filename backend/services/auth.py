from datetime import datetime, timezone
from typing import Annotated, Final

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError, IntegrityError
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
from dependencies.db import Session
from models.user import User
from schemas.auth import AccessToken, BaseToken, RefreshToken, TokenPair
from services.common import is_data_error
from services.users import create_user

# todo fix final typing
CREDENTIALS_EXCEPTION: Final[HTTPException] = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
)

TOKEN_IS_EXPIRED_EXCEPTION: Final[HTTPException] = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token is expired',
)

AUTH_EXCEPTION: Final[HTTPException] = HTTPException(
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
    except DBAPIError as e:
        if is_data_error(e):
            raise AUTH_EXCEPTION from e

        raise e

    user = result.one_or_none()
    if not user or not verify_password(password, user.password):
        raise AUTH_EXCEPTION

    return user


async def get_authenticated_token(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AccessToken:
    token_data = decode_and_get_token_data(token, AccessToken)

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions',
            )

    return token_data


async def get_current_user(
    session: Session,
    token: Annotated[AccessToken, Depends(get_authenticated_token)],
) -> User:
    user = await session.get(User, int(token.sub))
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user


async def get_user_from_refresh_token(
    session: AsyncSession,
    refresh_token: str,
) -> User:
    token_data = decode_and_get_token_data(refresh_token, RefreshToken)
    user = await session.get(User, int(token_data.sub))
    if user is None:
        raise CREDENTIALS_EXCEPTION

    if (
        user.last_refresh is None
        or user.last_refresh.timestamp() > token_data.iat
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is no longer active',
        )

    return user


def decode_and_get_token_data[T: BaseToken](token: str, model: type[T]) -> T:
    try:
        return model(**decode_token(token))
    except ExpiredSignatureError as e:
        raise TOKEN_IS_EXPIRED_EXCEPTION from e
    except (InvalidTokenError, ValidationError) as e:
        raise CREDENTIALS_EXCEPTION from e


async def login_user(
    session: AsyncSession,
    username: str,
    password: str,
    scopes: list[str] | None = None,
) -> TokenPair:
    user = await authenticate_user(session, username, password)
    return await issue_token_pair(session, user, scopes)


async def register_user(
    session: AsyncSession,
    username: str,
    password: str,
) -> TokenPair:
    try:
        user = await create_user(session, username, password)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is already taken',
        ) from e
    except DBAPIError as e:
        if is_data_error(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            ) from e

        raise e

    return await issue_token_pair(session, user)


async def issue_token_pair(
    session: AsyncSession,
    user: User,
    scopes: list[str] | None = None,
) -> TokenPair:
    payload: TokenData = _create_token_base_payload_for_user(user)

    available_scopes = _get_available_scopes_for_user(user)
    if scopes is not None:
        available_scopes = list(set(scopes) & set(available_scopes))

    user.last_refresh = datetime.now(timezone.utc)
    session.add(user)
    await session.commit()
    return TokenPair(
        access_token=create_access_token(payload, scopes=available_scopes),
        refresh_token=create_refresh_token(payload),
    )


async def refresh_tokens(
    session: AsyncSession,
    refresh_token: str,
) -> TokenPair:
    user = await get_user_from_refresh_token(session, refresh_token)
    payload: TokenData = {'sub': str(user.id)}
    scopes = _get_available_scopes_for_user(user)
    user.last_refresh = datetime.now(timezone.utc)
    token_pair = TokenPair(
        access_token=create_access_token(payload, scopes=scopes),
        refresh_token=create_refresh_token(payload),
    )
    session.add(user)
    await session.commit()

    return token_pair


def _create_token_base_payload_for_user(user: User) -> TokenData:
    return {'sub': str(user.id)}


def _get_available_scopes_for_user(user: User) -> list[str]:
    scopes: list[str] = []
    if user.is_admin:
        scopes.append('admin')

    return scopes
