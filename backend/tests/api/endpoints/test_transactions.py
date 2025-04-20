from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.transaction import TransactionCategory


async def test_create_category(
    session: AsyncSession,
    admin_client: AsyncClient,
) -> None:
    payload = {'name': 'Food'}
    response = await admin_client.post(
        '/api/v1/transactions/categories',
        json=payload,
    )
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == payload['name']

    category_query = select(TransactionCategory).where(
        TransactionCategory.id == data['id'],
    )
    category = (await session.exec(category_query)).one_or_none()
    assert category is not None


async def test_update_category(
    session: AsyncSession,
    admin_client: AsyncClient,
) -> None:
    category = TransactionCategory(name='Old')
    session.add(category)
    await session.commit()
    await session.refresh(category)

    update_data = {'name': 'New'}
    response = await admin_client.patch(
        f'/api/v1/transactions/categories/{category.id}',
        json=update_data,
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated['name'] == 'New'


async def test_delete_category(
    session: AsyncSession,
    admin_client: AsyncClient,
) -> None:
    category = TransactionCategory(name='ToDelete')
    session.add(category)
    await session.commit()
    await session.refresh(category)

    response = await admin_client.delete(
        f'/api/v1/transactions/categories/{category.id}',
    )
    assert response.status_code == 204

    deleted_query = select(TransactionCategory).where(
        TransactionCategory.id == category.id,
    )
    deleted = (await session.exec(deleted_query)).one_or_none()

    assert deleted is None


async def test_all_categories(
    session: AsyncSession,
    admin_client: AsyncClient,
) -> None:
    session.add_all(
        [
            TransactionCategory(name='Cat1'),
            TransactionCategory(name='Cat2'),
        ],
    )
    await session.commit()

    response = await admin_client.get('/api/v1/transactions/categories')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
