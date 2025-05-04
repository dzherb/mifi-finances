from fastapi import APIRouter

from api.responses import UNAUTHORIZED
from dependencies.users import CurrentUser
from schemas.users import UserOut

router = APIRouter()


@router.get('/me', responses=UNAUTHORIZED)
async def me(user: CurrentUser) -> UserOut:
    return UserOut.model_validate(user)
