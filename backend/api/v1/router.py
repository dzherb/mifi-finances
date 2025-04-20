from fastapi import APIRouter

from api.v1.endpoints import auth, banks, ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix='/ping', tags=['ping'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(banks.router, prefix='/banks', tags=['banks'])
