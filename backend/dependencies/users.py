from typing import Annotated

from fastapi import Security

from models.user import User
from services.auth import get_current_user

CurrentUser = Annotated[User, Security(get_current_user)]
AdminUser = Annotated[User, Security(get_current_user, scopes=['admin'])]
