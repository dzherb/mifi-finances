from datetime import datetime, timezone
import typing
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine

from api.responses import FORBIDDEN, UNAUTHORIZED
from core.logging import logger
from dependencies.db import Session
from dependencies.users import AdminUser

router = APIRouter()


class Ping(BaseModel):
    ok: Literal[True] = True


class PingExpanded(Ping):
    database: str
    current_user: str
    server_time: datetime


@router.get('')
async def ping() -> Ping:
    logger.info('ping')
    return Ping()


@router.get(
    path='/extra',
    responses=UNAUTHORIZED | FORBIDDEN,
)
async def ping_extra(session: Session, user: AdminUser) -> PingExpanded:
    engine = typing.cast(AsyncEngine, session.bind)
    return PingExpanded(
        database=engine.url.database,
        current_user=user.username,
        server_time=datetime.now(timezone.utc),
    )
