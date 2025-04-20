from fastapi import status
from httpx import AsyncClient
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from services.banks import create_bank


async def test_create_bank(admin_client: AsyncClient) -> None:
    response = await admin_client.post('/api/v1/banks', json={'name': 'Bank1'})
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data['name'] == 'Bank1'
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert 'updated_at' in response_data


async def test_cant_create_bank_with_the_same_name(
    admin_client: AsyncClient,
) -> None:
    response = await admin_client.post('/api/v1/banks', json={'name': 'Bank1'})
    assert response.status_code == status.HTTP_201_CREATED

    response = await admin_client.post('/api/v1/banks', json={'name': 'Bank1'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    'request_data,response_name',
    (
        ({'name': 'BankNew'}, 'BankNew'),
        ({'name': None}, 'Bank1'),
    ),
)
async def test_update_bank(
    admin_client: AsyncClient,
    session: AsyncSession,
    request_data: dict[str, str | None],
    response_name: str,
) -> None:
    bank = await create_bank(session, name='Bank1')

    response = await admin_client.patch(
        f'/api/v1/banks/{bank.id}',
        json=request_data,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['name'] == response_name
    assert 'id' in response_data
    assert 'created_at' in response_data
    assert 'updated_at' in response_data
