import schemathesis
from schemathesis import Case

schemathesis.experimental.OPEN_API_3_1.enable()
schema = schemathesis.from_pytest_fixture('openapi')


@schema.parametrize()
def test_api(case: Case) -> None:
    case.call_and_validate()
