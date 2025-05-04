from sqlmodel.ext.asyncio.session import AsyncSession

from core.security import hash_password
from models.user import User
from services.crud import BaseCRUD


class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.model = User


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.crud = UserCRUD(session)

    async def create_user(
        self,
        username: str,
        password: str,
        is_admin: bool = False,
    ) -> User:
        user = User(
            username=username,
            password=hash_password(password),
            is_admin=is_admin,
        )

        return await self.crud.create(user)


async def create_user(
    session: AsyncSession,
    username: str,
    password: str,
    is_admin: bool = False,
) -> User:
    """This function exists because user creation is currently
    done in many places. These usages should eventually be
    refactored to use UserService directly.
    """
    return await UserService(session).create_user(username, password, is_admin)
