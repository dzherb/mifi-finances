from collections.abc import Callable, Iterable
from typing import (
    Annotated,
    cast,
    Literal,
    TYPE_CHECKING,
)

from fastapi import HTTPException, status
from fastapi.params import Query

from services.crud import OrderByItem


def order_by_dependency(
    fields: Iterable[str],
    default: Iterable[str] | None = None,
) -> Callable[[list[str]], list[OrderByItem]]:
    all_options = []
    for field in fields:
        all_options.append(field)
        all_options.append('-' + field)

    if TYPE_CHECKING:
        type_ = list[str]
    else:
        type_ = list[Literal[tuple(all_options)]]

    if default is None:
        default = []

    final_default = cast(list[str], default)

    def _get_order_by(
        order_by: Annotated[type_, Query()] = final_default,
    ) -> list[OrderByItem]:
        _validate_order_by(order_by)
        return [_parse_order_by_string(item) for item in order_by]

    return _get_order_by


def _validate_order_by(items: Iterable[str]) -> None:
    seen = set()

    for item in items:
        item_real = item[1:] if item.startswith('-') else item
        if item_real in seen:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order field '{item_real}' is ambiguous",
            )

        seen.add(item)


def _parse_order_by_string(order_by: str) -> OrderByItem:
    order_by = order_by.strip()

    desc = order_by.startswith('-')
    field = order_by.lstrip('-')

    return OrderByItem(field=field, desc=desc)
