from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query

from api.responses import UNAUTHORIZED
from dependencies.db import Session
from dependencies.users import CurrentUser
from schemas.analytics import DynamicsByInterval, Interval, StartEnd
from services.analytics.analytics import DynamicsByIntervalService

router = APIRouter()


class QueryParams(StartEnd):
    interval: Interval


@router.get(
    path='/dynamics_by_interval',
    responses=UNAUTHORIZED,
)
async def dynamics_by_interval(
    session: Session,
    user: CurrentUser,
    params: Annotated[QueryParams, Query()],
) -> DynamicsByInterval:
    service = DynamicsByIntervalService(session, user)
    return await service.get(
        start=params.start,
        end=params.end,
        interval=params.interval,
    )
