from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from db.session import get_session

router = APIRouter()


class Ping(BaseModel):
    ok: bool


@router.get('')
async def ping(session: Annotated[AsyncSession, Depends(get_session)]) -> Ping:
    return Ping(ok=True)
