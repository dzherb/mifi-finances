import typing

import schemathesis
from schemathesis import Case
from schemathesis.auths import AuthContext
from starlette.types import ASGIApp
from starlette_testclient import TestClient

schemathesis.experimental.OPEN_API_3_1.enable()
schema = schemathesis.from_pytest_fixture('openapi_for_schemathesis')

TOKEN_ENDPOINT = '/api/v1/auth/login'
USERNAME = 'admin'
PASSWORD = 'password'


@schema.auth()
class SchemaAuth:
    def get(self, case: Case, context: AuthContext) -> str:
        app: ASGIApp = typing.cast(ASGIApp, context.app)
        client = TestClient(app)
        response = client.post(
            TOKEN_ENDPOINT,
            json={'username': USERNAME, 'password': PASSWORD},
        )
        result: dict[str, str] = response.json()
        return result['access_token']

    def set(self, case: Case, data: str, context: AuthContext) -> None:
        case.headers = case.headers or {}
        case.headers['Authorization'] = f'Bearer {data}'


@schema.parametrize()
def test_api(case: Case) -> None:
    case.call_and_validate()
