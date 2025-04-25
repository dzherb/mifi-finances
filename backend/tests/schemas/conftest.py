from fastapi import FastAPI
import pytest
import schemathesis
from schemathesis.specs.openapi.schemas import BaseOpenAPISchema

from models.user import User


@pytest.fixture
async def openapi_for_schemathesis(
    app: FastAPI,
    admin_user: User,
) -> BaseOpenAPISchema:
    return schemathesis.from_asgi('/openapi.json', app)
