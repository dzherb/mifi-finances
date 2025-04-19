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
    decode_and_get_token_data,
    get_authenticated_token,
    get_current_user,
    get_user_from_refresh_token,
    login_user,
    refresh_tokens,
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
    token_data = await get_authenticated_token(
        SecurityScopes(scopes=['admin']),
        token,
    )
    user_out = await get_current_user(
        session=session,
        token=token_data,
    )

    assert user_out.id == admin_user.id


async def test_get_current_user_fail_on_user_absence(
    session: AsyncSession,
) -> None:
    token = create_access_token({'sub': '1'}, scopes=['admin'])
    token_data = await get_authenticated_token(SecurityScopes(), token)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(
            session=session,
            token=token_data,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == CREDENTIALS_EXCEPTION.detail


async def test_get_authenticated_token_forbidden(
    session: AsyncSession,
    admin_user: User,
) -> None:
    # create token with no admin scope
    token = create_access_token({'sub': str(admin_user.id)})
    with pytest.raises(HTTPException) as exc:
        await get_authenticated_token(SecurityScopes(scopes=['admin']), token)

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
    token_pair = await login_user(session, 'user', 'password')
    access_token_data = decode_and_get_token_data(
        token_pair.access_token,
        AccessToken,
    )
    refresh_token_data = decode_and_get_token_data(
        token_pair.refresh_token,
        RefreshToken,
    )

    assert access_token_data.sub == str(user.id)
    assert refresh_token_data.sub == str(user.id)


@pytest.mark.parametrize(
    'scopes,expected_scopes',
    (
        (None, ['admin']),
        ([], []),
        (['something', 'else'], []),
        (['admin'], ['admin']),
        (['admin', 'something', 'else'], ['admin']),
    ),
)
async def test_can_limit_scopes_on_login(
    session: AsyncSession,
    admin_user: User,
    scopes: list[str],
    expected_scopes: list[str],
) -> None:
    token_pair = await login_user(session, 'admin', 'password', scopes=scopes)
    access_token_data = decode_and_get_token_data(
        token_pair.access_token,
        AccessToken,
    )
    assert access_token_data.scopes == expected_scopes


async def test_tokens_refresh_success(
    session: AsyncSession,
    user: User,
) -> None:
    old_token_pair = await login_user(session, 'user', 'password')
    new_token_pair = await refresh_tokens(
        session,
        old_token_pair.refresh_token,
    )

    access_token = await get_authenticated_token(
        SecurityScopes(),
        new_token_pair.access_token,
    )
    user_from_token = await get_current_user(
        session,
        access_token,
    )
    assert user_from_token.id == user.id


async def test_tokens_refresh_fail_on_second_attempt(
    session: AsyncSession,
    user: User,
) -> None:
    old_token_pair = await login_user(session, 'user', 'password')
    await refresh_tokens(session, old_token_pair.refresh_token)

    with pytest.raises(HTTPException) as exc:
        await refresh_tokens(session, old_token_pair.refresh_token)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == 'Token is no longer active'
