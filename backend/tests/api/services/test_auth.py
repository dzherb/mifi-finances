from datetime import datetime, timedelta, timezone
from unittest import mock

from fastapi import HTTPException, status
from fastapi.security import SecurityScopes
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    TokenData,
)
from models.user import User
from schemas.auth import AccessToken, RefreshToken
from services.auth import (
    AUTH_EXCEPTION,
    authenticate_user,
    CREDENTIALS_EXCEPTION,
    get_current_user,
    get_token_data,
    get_user_from_refresh_token,
    login_user,
)


async def test_authenticate_user_success(session: AsyncSession) -> None:
    user = User(username='alice', password=hash_password('correct_password'))
    session.add(user)
    await session.commit()

    result = await authenticate_user(session, 'alice', 'correct_password')
    assert result.username == 'alice'


async def test_authenticate_user_fail(session: AsyncSession) -> None:
    user = User(username='bob', password=hash_password('password'))
    session.add(user)
    await session.commit()

    with pytest.raises(HTTPException) as exc:
        await authenticate_user(session, 'bob', 'bad_password')

    assert exc.value.detail == AUTH_EXCEPTION.detail


async def test_get_current_user_success(
    session: AsyncSession,
    admin_user: User,
) -> None:
    token = create_access_token({'sub': str(admin_user.id)}, scopes=['admin'])
    user_out = await get_current_user(
        security_scopes=SecurityScopes(scopes=['admin']),
        session=session,
        token=token,
    )

    assert user_out.id == admin_user.id


async def test_get_current_user_fail_on_user_absence(
    session: AsyncSession,
) -> None:
    token = create_access_token({'sub': '1'}, scopes=['admin'])
    with pytest.raises(HTTPException) as exc:
        await get_current_user(
            security_scopes=SecurityScopes(scopes=['admin']),
            session=session,
            token=token,
        )
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == CREDENTIALS_EXCEPTION.detail


async def test_get_current_user_forbidden(
    session: AsyncSession,
    admin_user: User,
) -> None:
    # create token with no admin scope
    token = create_access_token({'sub': str(admin_user.id)})
    with pytest.raises(HTTPException) as exc:
        await get_current_user(
            security_scopes=SecurityScopes(scopes=['admin']),
            session=session,
            token=token,
        )
        assert exc.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc.value.detail == 'Not enough permissions'


async def test_get_user_from_refresh_token_success(
    session: AsyncSession,
) -> None:
    now = datetime.now(timezone.utc)
    user = User(username='refreshguy', password='hashed', last_refresh=now)
    session.add(user)
    await session.commit()

    token = create_refresh_token({'sub': str(user.id)})

    result = await get_user_from_refresh_token(session, token)
    assert result.username == 'refreshguy'


async def test_get_user_from_refresh_token_expired(
    session: AsyncSession,
) -> None:
    now = datetime.now(timezone.utc)
    user = User(username='oldman', password='hashed', last_refresh=now)
    session.add(user)
    await session.commit()

    payload: TokenData = {'sub': str(user.id)}

    with mock.patch('core.security.datetime') as mock_now:
        mock_now.now.return_value = now - timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )
        token = create_refresh_token(payload)

    with pytest.raises(HTTPException) as exc:
        await get_user_from_refresh_token(session, token)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == 'Token is expired'


async def test_login_user_returns_correct_tokens(
    session: AsyncSession,
    user: User,
) -> None:
    pair = await login_user(session, 'user', 'password')
    access_token_data = get_token_data(pair.access_token, AccessToken)
    refresh_token_data = get_token_data(pair.refresh_token, RefreshToken)

    assert access_token_data.sub == str(user.id)
    assert refresh_token_data.sub == str(user.id)
