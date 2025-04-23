# ruff: noqa: RUF001, PT011
import pytest

from core.validators import validate_inn

VALID_INNS = [
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

INVALID_INNS = [
    '234432432',
    '423543534553',
    '123455342554321',
    'аыав432ыавыавы',
    '11150уц09301',
    '1110005080',
    '4234324324',
    '54654645666',
    '1112427095',
    '1114327151',
    '1111111111',
    '',
    '123456789',
    '1234567890123',
]


@pytest.mark.parametrize('inn', VALID_INNS)
def test_valid_inns(inn: str) -> None:
    assert validate_inn(inn) == inn


@pytest.mark.parametrize('inn', INVALID_INNS)
def test_invalid_inns(inn: str) -> None:
    with pytest.raises(ValueError):
        validate_inn(inn)
