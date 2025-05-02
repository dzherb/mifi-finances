from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query

from api.responses import UNAUTHORIZED
from dependencies.users import CurrentUser
from schemas.analytics import DynamicsByPeriod, Period

router = APIRouter()


@router.get(
    path='/dynamics_by_period',
    responses=UNAUTHORIZED,
)
async def dynamics_by_period(
    user: CurrentUser,
    period: Annotated[Period, Query()],
) -> DynamicsByPeriod:
    """potom"""
