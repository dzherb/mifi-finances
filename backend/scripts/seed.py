import argparse
from collections.abc import Generator
from contextlib import contextmanager, redirect_stdout
from datetime import datetime
import os
import sys
import warnings

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import asyncio

from faker import Faker
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.session import create_async_engine, create_async_session_factory
from models.bank import Bank
from models.transaction import (
    PartyType,
    Transaction,
    TransactionCategory,
    TransactionStatus,
    TransactionType,
)
from models.user import User

faker = Faker(locale='ru-RU')
faker.seed_instance(2)

BANKS_COUNT = 10
CATEGORIES_COUNT = 10
USERS_COUNT = 10
TRANSACTIONS_COUNT = 200

INNS = [
    '6449013711',
    '3664069397',
    '4205001725',
    '7743880975',
    '300504899258',
    '6447207743',
    '4205036090',
    '4205046123',
    '0660534489',
    '4205060689',
    '3694555299',
    '4205109214',
    '4207003319',
    '4207008719',
    '635277570478',
    '451408304546',
    '079285641150',
    '793970318200',
    '459147066360',
    '722433057002',
    '499918818482',
    '383391302210',
    '9198578814',
]


def create_timestamp() -> dict[str, datetime]:
    created_at = faker.date_time_this_year(before_now=True, after_now=False)
    updated_at = faker.date_time_between_dates(
        datetime_start=created_at,
        datetime_end=datetime.now(),
    )
    return {
        'created_at': created_at,
        'updated_at': updated_at,
    }


def create_transaction_timestamp() -> dict[str, datetime]:
    timestamp = create_timestamp()
    occurred_at = faker.date_time_between_dates(
        datetime_start=timestamp['created_at'],
        datetime_end=datetime.now(),
    )
    return {
        **timestamp,
        'occurred_at': occurred_at,
    }


async def create_banks(session: AsyncSession) -> list[Bank]:
    banks: list[Bank] = [
        Bank(
            name=faker.company(),
            **create_timestamp(),
        )
        for _ in range(BANKS_COUNT)
    ]

    session.add_all(banks)
    await session.commit()
    for bank in banks:
        await session.refresh(bank)
    return banks


async def create_categories(
    session: AsyncSession,
) -> list[TransactionCategory]:
    categories: list[TransactionCategory] = [
        TransactionCategory(name=faker.word(), **create_timestamp())
        for _ in range(CATEGORIES_COUNT)
    ]
    session.add_all(categories)
    await session.commit()
    for category in categories:
        await session.refresh(category)
    return categories


async def create_users(session: AsyncSession) -> list[User]:
    from services.users import create_user

    users: list[User] = []
    for _ in range(USERS_COUNT - 2):
        username = faker.user_name()
        password = username
        is_admin = faker.boolean(chance_of_getting_true=20)
        user = await create_user(
            session,
            username,
            password,
            is_admin,
        )
        users.append(user)

    admin = await create_user(session, 'admin', 'admin', True)
    user = await create_user(session, 'user', 'user', False)
    users.append(admin)
    users.append(user)

    return users


async def create_transactions(
    session: AsyncSession,
    users: list[User],
    banks: list[Bank],
    categories: list[TransactionCategory],
) -> None:
    transactions: list[Transaction] = []

    for _ in range(TRANSACTIONS_COUNT):
        user = faker.random_element(elements=users)
        sender_bank = faker.random_element(elements=banks)
        recipient_bank = faker.random_element(elements=banks)
        while recipient_bank.id == sender_bank.id:
            recipient_bank = faker.random_element(elements=banks)

        category = faker.random_element(elements=categories)

        transaction = Transaction(
            recipient_phone=faker.numerify('+79#########'),
            recipient_inn=faker.random_element(elements=INNS),
            account_number=str(faker.random_int(min=100, max=100_000)),
            recipient_account_number=str(
                faker.random_int(min=100, max=100_000),
            ),
            amount=faker.random_int(min=100, max=100_000),
            transaction_type=faker.random_element(
                elements=list(TransactionType),
            ),
            status=faker.random_element(elements=list(TransactionStatus)),
            party_type=faker.random_element(elements=list(PartyType)),
            user_id=user.id,
            sender_bank_id=sender_bank.id,
            recipient_bank_id=recipient_bank.id,
            category_id=category.id,
            comment=faker.sentence(4),
            **create_transaction_timestamp(),
        )
        transactions.append(transaction)

    session.add_all(transactions)
    await session.commit()


async def clear_database(session: AsyncSession) -> None:
    # https://github.com/fastapi/sqlmodel/issues/909#issuecomment-2242435908
    # как вызвать .exec(), чтобы mypy не ругался?
    await session.execute(delete(Transaction))
    await session.execute(delete(User))
    await session.execute(delete(TransactionCategory))
    await session.execute(delete(Bank))
    await session.commit()


async def seed(clear_only: bool) -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = create_async_session_factory(engine)

    async with async_session() as session:
        await clear_database(session)

        if not clear_only:
            banks: list[Bank] = await create_banks(session)
            categories: list[TransactionCategory] = await create_categories(
                session,
            )
            users: list[User] = await create_users(session)
            await create_transactions(session, users, banks, categories)

    await engine.dispose()


@contextmanager
def supress_logs_and_warnings() -> Generator[None]:
    with (
        open(os.devnull, 'w') as fnull,
        redirect_stdout(fnull),
        warnings.catch_warnings(action='ignore'),
    ):
        yield


def confirm_action(message: str) -> bool:
    print(f'\n{message} (y/n)')  # noqa: T201
    try:
        confirm = input().strip().lower()
        return confirm == 'y'
    except KeyboardInterrupt:
        print('\nOperation cancelled.')  # noqa: T201
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description='Seed the database')
    parser.add_argument(
        '--clear',
        action='store_true',
        help='only clear the database without adding any data',
    )
    args = parser.parse_args()
    clear: bool = args.clear

    if clear:
        message = 'Database will be flushed. Are you sure?'
    else:
        message = 'Database will be flushed first. Are you sure?'

    if not confirm_action(message):
        print('Operation aborted.')  # noqa: T201
        sys.exit(0)

    print('\nRunning the script...')  # noqa: T201

    with supress_logs_and_warnings():
        asyncio.run(seed(clear_only=clear))

    print('Done.\n')  # noqa: T201


if __name__ == '__main__':
    main()
