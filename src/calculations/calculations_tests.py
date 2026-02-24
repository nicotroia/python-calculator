"""src/calculations/calculations.tests.py

Tests for the Calculation classes and CalculationFactory
"""
import pytest

from src.calculations.calculations import (
  CalculationFactory,
  Calculation,
)

@pytest.mark.parametrize(
  "ctype,a,b,expected_class,expected_result",
  [
    ("add", 2.0, 3.0, "AddCalculation", 5.0),
    ("subtract", 5.0, 3.0, "SubtractCalculation", 2.0),
    ("multiply", 4.0, 2.5, "MultiplyCalculation", 10.0),
    ("divide", 9.0, 3.0, "DivideCalculation", 3.0),
    ("power", 2.0, 3.0, "PowerCalculation", 8.0),
    ("root", 2.0, 9.0, "RootCalculation", 3.0),
  ],
)
def test_factory_creates_and_executes(ctype, a, b, expected_class, expected_result):
  calc = CalculationFactory.create_calculation(ctype, a, b)
  assert calc.__class__.__name__ == expected_class
  assert calc.execute() == expected_result


def test_str_and_repr_show_expected_values():
  calc = CalculationFactory.create_calculation("add", 2.0, 3.0)
  s = str(calc)
  assert s == "2.0 Add 3.0 = 5.0"
  # __repr__ should include the class name and operand values
  assert repr(calc) == "AddCalculation(a=2.0, b=3.0)"


def test_create_calculation_is_case_insensitive():
  calc = CalculationFactory.create_calculation("AdD", 1.0, 1.0)
  assert calc.__class__.__name__ == "AddCalculation"
  assert calc.execute() == 2.0


def test_unsupported_type_raises_with_available_list():
  with pytest.raises(ValueError) as exc:
    CalculationFactory.create_calculation("mod", 1.0, 2.0)
  msg = str(exc.value)
  assert "Unsupported calculation type" in msg
  # Ensure the error mentions available types
  assert "Available types" in msg


def test_registering_existing_type_raises():
  # Attempting to register an already-registered type should raise
  decorator = CalculationFactory.register_calculation("add")

  with pytest.raises(ValueError):
    # calling the decorator on a dynamically-created subclass triggers the check
    decorator(type("DummyAdd", (Calculation,), {"execute": lambda self: 0}))


def test_divide_by_zero_raises_from_divide_calculation():
  calc = CalculationFactory.create_calculation("divide", 1.0, 0.0)
  with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
    calc.execute()


def test_lbyl_vs_eafp_examples():
  # LBYL: check before executing
  safe_calc = CalculationFactory.create_calculation("divide", 10.0, 2.0)
  if safe_calc.b == 0:  # pragma: no cover
    pytest.skip("LBYL prevented division by zero")  # pragma: no cover
  else:
    assert safe_calc.execute() == 5.0

  # EAFP: attempt and handle exception
  unsafe_calc = CalculationFactory.create_calculation("divide", 5.0, 0.0)
  with pytest.raises(ZeroDivisionError):
    unsafe_calc.execute()
