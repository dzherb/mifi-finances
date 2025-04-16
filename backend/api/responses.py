from fastapi import status

from schemas.errors import MessageError

UNAUTHORIZED = {
    status.HTTP_401_UNAUTHORIZED: {
        'description': 'Unauthorized',
        'model': MessageError,
        'content': {
            'application/json': {
                'example': {'detail': 'Not authenticated'},
            },
        },
    },
}

FORBIDDEN = {
    status.HTTP_403_FORBIDDEN: {
        'description': 'Forbidden',
        'model': MessageError,
        'content': {
            'application/json': {
                'example': {'detail': 'Not enough permissions'},
            },
        },
    },
}
