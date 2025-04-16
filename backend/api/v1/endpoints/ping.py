from datetime import datetime, timezone
import typing
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from fastapi.params import Security
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from api.responses import FORBIDDEN, UNAUTHORIZED
from dependencies import get_session
from models.user import User
from services.auth import get_current_user

router = APIRouter()


class Ping(BaseModel):
    ok: Literal[True] = True


class PingExpanded(Ping):
    database: str
    current_user: str
    server_time: datetime


@router.get('')
async def ping() -> Ping:
    return Ping()


@router.get('/extra', responses={**UNAUTHORIZED, **FORBIDDEN})  # type: ignore
async def ping_extra(
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Security(get_current_user, scopes=['admin'])],
) -> PingExpanded:
    engine = typing.cast(AsyncEngine, session.bind)
    return PingExpanded(
        database=engine.url.database,
        current_user=user.username,
        server_time=datetime.now(timezone.utc),
    )
