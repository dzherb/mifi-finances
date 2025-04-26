from fastapi import HTTPException, status
import pytest

from models.transaction import (
    Transaction,
    TransactionStatus,
)
from models.user import User
from services.transactions import TransactionGuard


def test_editable_transaction_with_allowed_fields(
    transaction: Transaction,
    user: User,
) -> None:
    guard = TransactionGuard(transaction, user)
    guard.ensure_editable({'comment': 'Updated comment', 'amount': 150.0})


@pytest.mark.parametrize(
    'transaction_status',
    sorted(TransactionGuard.EDIT_FORBIDDEN_STATUSES),
)
def test_editable_transaction_with_forbidden_status(
    transaction_status: TransactionStatus,
    transaction: Transaction,
    user: User,
) -> None:
    transaction.status = transaction_status
    guard = TransactionGuard(transaction, user)

    with pytest.raises(HTTPException) as exc:
        guard.ensure_editable({'comment': 'New'})

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_editable_transaction_with_forbidden_field(
    transaction: Transaction,
    user: User,
) -> None:
    guard = TransactionGuard(transaction, user)

    with pytest.raises(HTTPException) as exc:
        guard.ensure_editable({'not_allowed_field': 'value'})

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_editable_transaction_with_wrong_user(
    transaction: Transaction,
) -> None:
    other_user = User(id=99, is_admin=False, password='...')
    guard = TransactionGuard(transaction, other_user)

    with pytest.raises(HTTPException) as exc:
        guard.ensure_editable({'comment': 'try update'})

    assert exc.value.status_code == status.HTTP_403_FORBIDDEN


def test_editable_transaction_by_admin(
    transaction: Transaction,
    admin_user: User,
) -> None:
    assert transaction.user_id != admin_user.id

    guard = TransactionGuard(transaction, admin_user)
    guard.ensure_editable({'comment': 'admin update'})


@pytest.mark.parametrize(
    'transaction_status',
    sorted(TransactionGuard.DELETE_FORBIDDEN_STATUSES),
)
def test_deletable_transaction_with_forbidden_status(
    transaction_status: TransactionStatus,
    transaction: Transaction,
    user: User,
) -> None:
    transaction.status = transaction_status
    guard = TransactionGuard(transaction, user)

    with pytest.raises(HTTPException) as exc:
        guard.ensure_deletable()

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_deletable_transaction_with_wrong_user(
    transaction: Transaction,
) -> None:
    other_user = User(id=99, is_admin=False, password='...')
    guard = TransactionGuard(transaction, other_user)

    with pytest.raises(HTTPException) as exc:
        guard.ensure_deletable()

    assert exc.value.status_code == status.HTTP_403_FORBIDDEN


def test_deletable_transaction_by_admin(
    transaction: Transaction,
    admin_user: User,
) -> None:
    assert transaction.user_id != admin_user.id

    guard = TransactionGuard(transaction, admin_user)
    guard.ensure_deletable()


def test_transaction_includes_allowed_update_fields() -> None:
    for field in TransactionGuard.ALLOWED_UPDATE_FIELDS:
        assert hasattr(Transaction, field)
