from functools import lru_cache
from pathlib import Path
from typing import ClassVar

from sqlalchemy import text, TextClause
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from models.user import User


class BaseAnalytics:
    QUERIES_DIR: ClassVar[Path] = (
        settings.BASE_DIR / 'services' / 'analytics' / 'queries'
    )

    query_template: ClassVar[Path | None] = None

    def __init__(self, session: AsyncSession, user: User):
        self.session = session
        self.user = user

    def get_query(self) -> TextClause:
        return _load_query(self.query_template)


@lru_cache
def _load_query(filepath: Path) -> TextClause:
    with open(filepath, 'r') as f:
        return text(f.read())
