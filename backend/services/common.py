from asyncpg import DataError as AsyncpgDataError
from sqlalchemy.exc import DataError, DBAPIError


def is_data_error(exc: DBAPIError) -> bool:
    if isinstance(exc, DataError):
        return True

    if exc.orig:
        return isinstance(exc.orig.__cause__, AsyncpgDataError)

    return False
