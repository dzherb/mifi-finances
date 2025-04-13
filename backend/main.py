from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from core.config import settings
from db.session import create_async_engine, create_async_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.engine = create_async_engine(settings.DATABASE_URL)
    app.state.async_session = create_async_session_factory(app.state.engine)
    yield
    await app.state.engine.dispose()


app = FastAPI(
    title='Finances Manager API',
    version='0.1.0',
    description='',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/api/v1')
