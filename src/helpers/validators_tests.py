""" src/helpers/validators_tests.py """
from decimal import Decimal
import pytest
from src.helpers.validators import InputValidator, ValidationError


def test_validate_integer_string():
  assert InputValidator.validate_number("42") == Decimal("42")


def test_validate_float_string():
  assert InputValidator.validate_number("3.14") == Decimal("3.14")


def test_validate_negative_string():
  assert InputValidator.validate_number("-7") == Decimal("-7")


def test_validate_strips_whitespace():
  assert InputValidator.validate_number("  10  ") == Decimal("10")


def test_validate_int_type():
  assert InputValidator.validate_number(5) == Decimal("5")


def test_validate_float_type():
  assert InputValidator.validate_number(1.5) == Decimal("1.5")


def test_validate_decimal_type():
  assert InputValidator.validate_number(Decimal("2.5")) == Decimal("2.5")


def test_validate_exceeds_max():
  with pytest.raises(ValidationError, match="exceeds maximum"):
    InputValidator.validate_number("999", max_input_value=Decimal("100"))


def test_validate_invalid_format():
  with pytest.raises(ValidationError, match="Invalid number format"):
    InputValidator.validate_number("abc")


def test_validate_empty_string():
  with pytest.raises(ValidationError, match="Invalid number format"):
    InputValidator.validate_number("")


def test_validate_none():
  with pytest.raises(ValidationError, match="Invalid number format"):
    InputValidator.validate_number(None)
