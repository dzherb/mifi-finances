from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, model_validator

from schemas.banks import BankOutShort
from schemas.transactions import TransactionCategoryOutShort


class Period(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end < self.start:
            raise ValueError('End time must not be earlier than start time')

        return self


class DynamicsByPeriodEntry(BaseModel):
    timestamp: datetime
    count: int


class DynamicsByPeriod(BaseModel):
    start: datetime
    end: datetime

    total_transactions: int
    credit_transactions: int
    debit_transactions: int


class DynamicsByType(BaseModel):
    start: datetime
    end: datetime

    total_transactions: int
    total_funds: Decimal


class ReceivedAndSpentComparison(BaseModel):
    start: datetime
    end: datetime

    total_received: Decimal
    total_spent: Decimal
    received_to_spent: Decimal


class DynamicsByStatus(BaseModel):
    start: datetime
    end: datetime

    total_successful_transactions: int
    total_cancelled_transactions: int


class BankStatistics(BaseModel):
    bank: BankOutShort
    total_transactions: int
    total_funds: Decimal


class DynamicsByBanks(BaseModel):
    start: datetime
    end: datetime

    sender_banks: list[BankStatistics]
    recipient_banks: list[BankStatistics]


class CategoryStatistics(BaseModel):
    category: TransactionCategoryOutShort
    total_transactions: int
    total_funds: Decimal


class DynamicsByCategories(BaseModel):
    start: datetime
    end: datetime

    spending_categories: list[CategoryStatistics]
    income_categories: list[CategoryStatistics]
