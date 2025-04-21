import os

import pytest

from core.config import settings


@pytest.fixture(scope='session')
def db_url() -> str:
    return os.getenv('TEST_DATABASE_URL', settings.DATABASE_URL)
