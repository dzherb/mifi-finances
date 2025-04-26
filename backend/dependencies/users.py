from typing import Annotated

from fastapi import Security

from models.user import User
from services.auth import get_authenticated_token, get_current_user

user_token_dependency = Security(get_authenticated_token)
admin_token_dependency = Security(get_authenticated_token, scopes=['admin'])

CurrentUser = Annotated[User, Security(get_current_user)]
AdminUser = Annotated[User, Security(get_current_user, scopes=['admin'])]
