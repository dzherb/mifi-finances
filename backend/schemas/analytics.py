from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Final, Self

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, model_validator

from schemas.banks import BankOutShort
from schemas.transactions import TransactionCategoryOutShort

MIN_DATETIME: Final = date(year=2010, month=1, day=1)
MAX_DATETIME: Final = (date.today() + relativedelta(years=5)).replace(
    month=1,
    day=1,
)


class StartEnd(BaseModel):
    start: date = Field(ge=MIN_DATETIME)
    end: date = Field(le=MAX_DATETIME)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end < self.start:
            raise ValueError('end time must not be earlier than start time')

        return self


class Interval(str, Enum):
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'


class DynamicsByIntervalEntry(BaseModel):
    date: date
    count: int


class DynamicsByInterval(StartEnd):
    interval: Interval
    entries: list[DynamicsByIntervalEntry]


class DynamicsByType(StartEnd):
    total_transactions: int
    total_funds: Decimal


class ReceivedAndSpentComparison(StartEnd):
    total_received: Decimal
    total_spent: Decimal
    received_to_spent: Decimal


class DynamicsByStatus(StartEnd):
    total_successful_transactions: int
    total_cancelled_transactions: int


class BankStatistics(BaseModel):
    bank: BankOutShort
    total_transactions: int
    total_funds: Decimal


class DynamicsByBanks(StartEnd):
    sender_banks: list[BankStatistics]
    recipient_banks: list[BankStatistics]


class CategoryStatistics(BaseModel):
    category: TransactionCategoryOutShort
    total_transactions: int
    total_funds: Decimal


class DynamicsByCategories(StartEnd):
    spending_categories: list[CategoryStatistics]
    income_categories: list[CategoryStatistics]
