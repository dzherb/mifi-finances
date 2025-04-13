from typing import Generator

from alembic.config import Config
import pytest

from tests.utils import get_alembic_config, tmp_database


@pytest.fixture
def db(db_url: str) -> Generator[str]:
    with tmp_database(db_url, 'pytest') as tmp_url:
        yield tmp_url


@pytest.fixture
def alembic_config(db: str) -> Generator[Config]:
    yield get_alembic_config(db)
