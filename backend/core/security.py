from datetime import datetime, timedelta, timezone
import typing

import bcrypt
from fastapi.security import OAuth2PasswordBearer
import jwt

from core.config import settings

ALGORITHM = 'HS256'


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    scopes={
        'admin': 'Administrator privileges',
    },
)


type TokenData = dict[str, str | int | float | bool | list[str]]


def create_access_token(
    data: TokenData,
    scopes: list[str] | None = None,
) -> str:
    if scopes is None:
        scopes = []

    issued_at = datetime.now(timezone.utc)
    to_encode = data.copy()
    expires_at = issued_at + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    to_encode.update(
        {
            'iat': issued_at.timestamp(),
            'exp': expires_at.timestamp(),
            'type': 'access',
            'scopes': scopes,
        },
    )
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: TokenData) -> str:
    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = data.copy()
    to_encode.update(
        {
            'iat': issued_at.timestamp(),
            'exp': expires_at.timestamp(),
            'type': 'refresh',
        },
    )
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password=plain.encode(),
        hashed_password=hashed.encode(),
    )


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password.encode(), salt=salt)
    return hashed_password.decode()


def decode_token(token: str) -> TokenData:
    token_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return typing.cast(TokenData, token_data)
