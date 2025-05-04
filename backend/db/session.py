from sqlalchemy import AsyncAdaptedQueuePool, Pool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db import pg_custom_types


def create_async_engine(
    database_url: str,
    pool_class: type[Pool] = AsyncAdaptedQueuePool,
) -> AsyncEngine:
    engine = _create_async_engine(
        database_url,
        echo=settings.DEBUG,
        future=True,
        poolclass=pool_class,
    )

    pg_custom_types.register(
        engine=engine,
        types=(pg_custom_types.Interval(),),
    )

    return engine


def create_async_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
