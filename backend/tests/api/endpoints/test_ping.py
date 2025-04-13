from httpx import AsyncClient


async def test_ping(client: AsyncClient, migrated_db: str) -> None:
    response = await client.get('/api/v1/ping')
    assert response.status_code == 200
    assert response.json() == {'ok': True, 'database': migrated_db.split('/')[-1]}
