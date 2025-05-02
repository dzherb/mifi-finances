from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User
from schemas.analytics import DynamicsByPeriod


class BaseAnalytics:
    def __init__(self, session: AsyncSession, user: User):
        self.session = session
        self.user = user


class DynamicsByPeriodAnalytics(BaseAnalytics):
    async def get(
        self,
        start: datetime,
        end: datetime,
    ) -> DynamicsByPeriod: ...
