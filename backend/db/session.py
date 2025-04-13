from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


def create_async_engine(database_url: str) -> AsyncEngine:
    return _create_async_engine(database_url, echo=True, future=True)


def create_async_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
