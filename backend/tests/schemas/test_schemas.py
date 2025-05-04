from contextlib import nullcontext
from datetime import date, datetime, timedelta

from pydantic import ValidationError
import pytest

from schemas.analytics import StartEnd


@pytest.mark.parametrize(
    ('start', 'end', 'fails'),
    [
        (date.today(), date.today() - timedelta(days=5), True),
        (date.today(), date.today(), False),
        (date.today(), date.today() + timedelta(days=5), False),
    ],
)
def test_start_end_schema(
    start: datetime,
    end: datetime,
    fails: bool,
) -> None:
    manager = pytest.raises(ValidationError) if fails else nullcontext()
    with manager:
        StartEnd(start=start, end=end)
