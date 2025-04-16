from sqlmodel.ext.asyncio.session import AsyncSession

from core.security import hash_password
from models.user import User


async def create_user(
    session: AsyncSession,
    username: str,
    password: str,
    is_admin: bool = False,
) -> User:
    user = User(
        username=username,
        password=hash_password(password),
        is_admin=is_admin,
    )
    session.add(user)
    await session.commit()
    return user
