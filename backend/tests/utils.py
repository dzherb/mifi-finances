from collections.abc import Generator
from contextlib import contextmanager
from urllib.parse import urlparse, urlunparse
import uuid

from alembic.config import Config
from sqlalchemy_utils import create_database, drop_database  # type: ignore


@contextmanager
def tmp_database(
    db_url: str,
    suffix: str = '',
    template: str | None = None,
) -> Generator[str]:
    tmp_db_name = '.'.join([uuid.uuid4().hex, suffix])
    parsed = urlparse(db_url)
    updated = parsed._replace(
        scheme='postgresql+psycopg',
        path=f'/{tmp_db_name}',
    )
    tmp_db_url: str = urlunparse(updated)
    create_database(tmp_db_url, template=template)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


def get_alembic_config(db_url: str = '') -> Config:
    config = Config('alembic.ini')
    config.set_main_option('sqlalchemy.url', db_url)
    return config
