from fastapi import status
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    'login,password,expected_status',
    (
        ('user', 'password', status.HTTP_200_OK),
        ('someone_else', 'password', status.HTTP_401_UNAUTHORIZED),
        ('user', 'wrong_password', status.HTTP_401_UNAUTHORIZED),
    ),
)
@pytest.mark.usefixtures('user')
async def test_login(
    client: AsyncClient,
    login: str,
    password: str,
    expected_status: int,
) -> None:
    response = await client.post(
        url='/api/v1/auth/login',
        data={'username': login, 'password': password},
    )
    assert response.status_code == expected_status


@pytest.mark.usefixtures('user')
async def test_tokens_refresh(client: AsyncClient) -> None:
    response = await client.post(
        url='/api/v1/auth/login',
        data={'username': 'user', 'password': 'password'},
    )
    assert response.status_code == status.HTTP_200_OK
    tokens = response.json()
    refresh_token = tokens['refresh_token']
    assert 'access_token' in tokens

    response = await client.post(
        url='/api/v1/auth/refresh',
        json={'refresh_token': refresh_token},
    )
    assert response.status_code == status.HTTP_200_OK
    new_tokens = response.json()

    assert 'access_token' in new_tokens
    assert new_tokens['access_token'] != tokens['access_token']


async def test_tokens_refresh_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        '/api/v1/auth/refresh',
        json={'refresh_token': 'invalid.token.value'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_tokens_refresh_missing_token(client: AsyncClient) -> None:
    response = await client.post('/api/v1/auth/refresh')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures('user')
async def test_refresh_token_can_only_be_used_once(
    client: AsyncClient,
) -> None:
    login_response = await client.post(
        '/api/v1/auth/login',
        data={'username': 'user', 'password': 'password'},
    )
    assert login_response.status_code == status.HTTP_200_OK
    refresh_token = login_response.json()['refresh_token']

    first_refresh = await client.post(
        '/api/v1/auth/refresh',
        json={'refresh_token': refresh_token},
    )
    assert first_refresh.status_code == status.HTTP_200_OK
    assert 'access_token' in first_refresh.json()

    second_refresh = await client.post(
        '/api/v1/auth/refresh',
        json={'refresh_token': refresh_token},
    )
    assert second_refresh.status_code == status.HTTP_401_UNAUTHORIZED
    assert second_refresh.json()['detail'] == 'Token is no longer active'
