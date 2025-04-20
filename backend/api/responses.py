from typing import Any

from fastapi import status

from schemas.errors import MessageError

type _Response = dict[int | str, dict[str, Any]]

UNAUTHORIZED: _Response = {
    status.HTTP_401_UNAUTHORIZED: {
        'model': MessageError,
    },
}

FORBIDDEN: _Response = {
    status.HTTP_403_FORBIDDEN: {
        'model': MessageError,
    },
}

BAD_REQUEST: _Response = {
    status.HTTP_400_BAD_REQUEST: {
        'model': MessageError,
    },
}

NOT_FOUND: _Response = {
    status.HTTP_404_NOT_FOUND: {
        'model': MessageError,
    },
}
