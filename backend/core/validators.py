from typing import Annotated

from pydantic import AfterValidator


# https://info.gosuslugi.ru/articles/%D0%92%D0%B0%D0%BB%D0%B8%D0%B4%D0%B0%D1%86%D0%B8%D1%8F/
# 8-9 пункты
def validate_inn(value: str) -> str:
    if not value.isdigit():
        raise ValueError('INN must contain only digits')

    if len(value) not in (10, 12):
        raise ValueError('INN must contain 10 or 12 digits')

    digits = [int(c) for c in value]

    # ИП, пункт 8
    if len(digits) == 12:  # noqa: PLR2004
        weights_11 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum_11 = sum(
            w * d for w, d in zip(weights_11, digits[:-2], strict=False)
        )
        checksum_11 = (control_sum_11 % 11) % 10

        weights_12 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum_12 = sum(
            w * d for w, d in zip(weights_12, digits[:-1], strict=False)
        )
        checksum_12 = (control_sum_12 % 11) % 10

        if digits[-2] != checksum_11 or digits[-1] != checksum_12:
            raise ValueError('Incorrect INN')

    # Огранизация, пункт 9
    if len(digits) == 10:  # noqa: PLR2004
        weights = [2, 4, 10, 3, 5, 9, 4, 6, 8]
        control_sum = sum(
            w * d for w, d in zip(weights, digits[:-1], strict=False)
        )
        checksum = (control_sum % 11) % 10
        if digits[-1] != checksum:
            raise ValueError('Incorrect INN')

    return value


INN = Annotated[str, AfterValidator(validate_inn)]
