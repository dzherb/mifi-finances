from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager
import os
from urllib.parse import urlparse

from alembic import command
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.types import ASGIApp

from api.v1.router import api_router
from core.config import settings
from db.session import create_async_engine, create_async_session_factory
from models.user import User
from services.users import create_user
from tests.utils import get_alembic_config, tmp_database


@pytest.fixture(scope='session')
def db_url() -> str:
    return os.getenv('TEST_DATABASE_URL', settings.DATABASE_URL)


@pytest.fixture(scope='session')
def migrated_db_template(db_url: str) -> Generator[str]:
    """
    Creates temporary database and applies migrations.
    Database can be used as template to fast creation databases for tests.

    Has "session" scope, so is called only once per tests run.
    """
    with tmp_database(db_url, 'template') as tmp_url:
        command.upgrade(get_alembic_config(tmp_url), 'head')
        yield tmp_url


@pytest.fixture
def migrated_db(db_url: str, migrated_db_template: str) -> Generator[str]:
    """
    Quickly creates clean migrated database using temporary database as base.
    Use this fixture in tests that require migrated database.
    """
    template_db = urlparse(migrated_db_template).path.lstrip('/')
    with tmp_database(db_url, 'pytest', template=template_db) as tmp_url:
        yield tmp_url


@pytest.fixture
def engine(migrated_db: str) -> AsyncEngine:
    return create_async_engine(migrated_db)


@pytest.fixture
async def session_factory(
    engine: AsyncEngine,
) -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    yield create_async_session_factory(
        engine,
    )
    await engine.dispose()


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest.fixture
async def fastapi_app(
    engine: AsyncEngine,
    session_factory: async_sessionmaker[AsyncSession],
) -> ASGIApp:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.engine = engine
        app.state.async_session = session_factory
        yield

    app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
    app.include_router(api_router, prefix='/api/v1')
    return app


@pytest.fixture
async def app(
    fastapi_app: FastAPI,
) -> AsyncGenerator[ASGIApp]:
    # use LifespanManager to activate db connection
    async with LifespanManager(fastapi_app) as manager:
        yield manager.app


@pytest.fixture
async def user(session: AsyncSession) -> User:
    return await create_user(
        session,
        username='user',
        password='password',
    )


@pytest.fixture
async def admin_user(session: AsyncSession) -> User:
    return await create_user(
        session,
        username='admin',
        password='password',
        is_admin=True,
    )
