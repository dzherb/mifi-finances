from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Self

from pydantic import BaseModel, model_validator

from schemas.banks import BankOutShort
from schemas.transactions import TransactionCategoryOutShort


class StartEnd(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end < self.start:
            raise ValueError('end time must not be earlier than start time')

        return self


class Interval(str, Enum):
    WEEK = 'week'
    MONTH = 'moth'
    QUARTER = 'quarter'
    YEAR = 'year'


class DynamicsByIntervalEntry(BaseModel):
    timestamp: datetime
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
