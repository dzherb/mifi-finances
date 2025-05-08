from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import uvicorn
from uvicorn_loguru_integration import (  # type: ignore[import-untyped]
    run_uvicorn_loguru as run,
)

from api.v1.router import api_router
from core.config import settings
from core.logging import configure_logging
from db.session import create_async_engine, create_async_session_factory

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # pragma: no cover
    app.state.engine = create_async_engine(settings.DATABASE_URL)
    app.state.async_session = create_async_session_factory(app.state.engine)
    try:
        yield
    finally:
        await app.state.engine.dispose()


app = FastAPI(
    title='Finances Manager API',
    version='0.1.0',
    description='',
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/api/v1')


def main() -> None:  # pragma: no cover
    run(
        uvicorn.Config(
            'main:app',
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
        ),
    )


if __name__ == '__main__':
    main()
