from typing import Literal

from pydantic import BaseModel, Field


class BaseToken(BaseModel):
    iat: float
    exp: float
    sub: str


class AccessToken(BaseToken):
    type: Literal['access']
    scopes: list[str]


class RefreshToken(BaseToken):
    type: Literal['refresh']


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RegisterRequest(LoginRequest):
    pass
