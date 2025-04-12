from fastapi import APIRouter

from api.v1.endpoints import ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix='/ping', tags=['ping'])
