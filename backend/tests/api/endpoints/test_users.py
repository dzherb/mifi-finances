from typing import Any

from fastapi import status
from httpx import AsyncClient
import pytest
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    ('request_client', 'status_code', 'expected'),
    [
        (
            lf('authenticated_client'),
            status.HTTP_200_OK,
            {'id': lf('user.id'), 'username': 'user', 'is_admin': False},
        ),
        (
            lf('admin_client'),
            status.HTTP_200_OK,
            {'id': lf('admin_user.id'), 'username': 'admin', 'is_admin': True},
        ),
        (lf('client'), status.HTTP_401_UNAUTHORIZED, None),
    ],
)
async def test_current_user(
    request_client: AsyncClient,
    status_code: int,
    expected: dict[str, Any] | None,
) -> None:
    response = await request_client.get('/api/v1/users/me')
    assert response.status_code == status_code

    if expected is not None:
        assert response.json() == expected
