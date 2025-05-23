from fastapi import APIRouter

from api.v1.endpoints import analytics, auth, banks, ping, transactions, users

api_router = APIRouter()
api_router.include_router(ping.router, prefix='/ping', tags=['ping'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(banks.router, prefix='/banks', tags=['banks'])
api_router.include_router(
    transactions.router,
    prefix='/transactions',
    tags=['transactions'],
)
api_router.include_router(
    analytics.router,
    prefix='/analytics',
    tags=['analytics'],
)
