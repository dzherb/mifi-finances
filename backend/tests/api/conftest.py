from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Generator
from urllib.parse import urlparse

from alembic import command
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
import httpx
from httpx import ASGITransport, AsyncClient
import pytest
from starlette.types import ASGIApp

from api.v1.router import api_router
from db.session import create_async_engine, create_async_session_factory
from tests.utils import get_alembic_config, tmp_database


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
async def app(migrated_db: str) -> AsyncGenerator[ASGIApp]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        app.state.engine = create_async_engine(migrated_db)
        app.state.async_session = create_async_session_factory(
            app.state.engine,
        )
        yield
        await app.state.engine.dispose()

    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router, prefix='/api/v1')

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture
async def client(app: ASGIApp) -> AsyncGenerator[AsyncClient]:
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test.com',
    ) as client:
        yield client
