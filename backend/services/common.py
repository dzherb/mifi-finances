from asyncpg import DataError as AsyncpgDataError
from sqlalchemy.exc import DataError, DBAPIError


def is_data_error(exc: DBAPIError) -> bool:
    # This is True when using psycopg
    if isinstance(exc, DataError):  # pragma: no cover
        return True

    # Check if it's an asyncpg error
    if exc.orig:
        return isinstance(exc.orig.__cause__, AsyncpgDataError)

    return False
