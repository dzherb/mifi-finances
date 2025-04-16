from fastapi import status
from httpx import AsyncClient


async def test_ping(client: AsyncClient) -> None:
    response = await client.get('/api/v1/ping')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'ok': True,
    }


async def test_ping_extra(admin_client: AsyncClient, migrated_db: str) -> None:
    response = await admin_client.get('/api/v1/ping/extra')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['ok'] is True
    assert data['database'] == migrated_db.split('/')[-1]
    assert data['current_user'] == 'test'


async def test_ping_extra_unauthorized(
    client: AsyncClient,
    migrated_db: str,
) -> None:
    response = await client.get('/api/v1/ping/extra')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
