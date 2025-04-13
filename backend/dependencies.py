from collections.abc import AsyncGenerator

from fastapi import Request
from sqlmodel.ext.asyncio.session import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    async with request.app.state.async_session() as session:
        yield session
