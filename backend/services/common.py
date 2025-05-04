from asyncpg import DataError as AsyncpgDataError
from sqlalchemy.exc import DataError, DBAPIError


def is_data_error(exc: DBAPIError) -> bool:
    # This is True while using psycopg
    if isinstance(exc, DataError):  # pragma: no cover
        return True

    if exc.orig:
        return isinstance(exc.orig.__cause__, AsyncpgDataError)

    return False
