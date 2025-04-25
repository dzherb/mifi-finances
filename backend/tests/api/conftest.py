from collections.abc import AsyncGenerator

import httpx
from httpx import ASGITransport, AsyncClient
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.types import ASGIApp

from models.user import User
from services.auth import login_user


@pytest.fixture
async def client(app: ASGIApp) -> AsyncGenerator[AsyncClient]:
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test.com',
    ) as client:
        yield client


@pytest.fixture
async def authenticated_client(
    session: AsyncSession,
    app: ASGIApp,
    user: User,
) -> AsyncGenerator[AsyncClient]:
    token_pair = await login_user(session, user.username, 'password')
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test.com',
        headers={'Authorization': f'Bearer {token_pair.access_token}'},
    ) as client:
        yield client


@pytest.fixture
async def admin_client(
    session: AsyncSession,
    app: ASGIApp,
    admin_user: User,
) -> AsyncGenerator[AsyncClient]:
    token_pair = await login_user(session, admin_user.username, 'password')
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test.com',
        headers={'Authorization': f'Bearer {token_pair.access_token}'},
    ) as client:
        yield client
