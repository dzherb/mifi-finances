from datetime import date, datetime, timedelta
import typing
from typing import Never

from dateutil.relativedelta import relativedelta

from schemas.analytics import DynamicsByInterval, Interval
from services.analytics.base import BaseAnalytics


class _StatementParams(typing.TypedDict):
    user_id: int
    start_date: date
    end_date: date
    interval_unit: Interval
    interval_value: timedelta | relativedelta


class DynamicsByIntervalService(BaseAnalytics):
    query_template = BaseAnalytics.QUERIES_DIR / 'dynamics_by_interval.sql'

    async def get(
        self,
        start: datetime,
        end: datetime,
        interval: Interval,
    ) -> DynamicsByInterval:
        result = await self.session.execute(
            self.get_query(),
            params=_StatementParams(
                user_id=typing.cast(int, self.user),
                start_date=start,
                end_date=end,
                interval_unit=interval,
                interval_value=self._get_delta(interval),
            ),
        )

        return DynamicsByInterval(
            start=start,
            end=end,
            interval=interval,
            entries=[r._mapping for r in result.all()],
        )

    def _get_delta(self, interval: Interval) -> relativedelta:
        match interval:
            case Interval.WEEK:
                return relativedelta(weeks=1)
            case Interval.MONTH:
                return relativedelta(months=1)
            case Interval.QUARTER:
                return relativedelta(months=3)
            case Interval.YEAR:
                return relativedelta(years=1)
            case _:
                # Ensure all cases are exhausted
                # otherwise mypy will throw an error
                _: Never = interval  # noqa: RET503
