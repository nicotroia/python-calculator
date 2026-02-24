""" src/operations/operations.tests.py """
import pytest
from src.operations.operations import Operations

def test_add_positive():
  """Test positive cases for add."""
  assert Operations.add(2, 3) == 5
  assert Operations.add(0, 0) == 0
  assert Operations.add(-1, 1) == 0

def test_add_negative():
  """Test negative cases for add."""
  assert Operations.add(-2, -3) == -5
  assert Operations.add(-1, 0) == -1

def test_subtract_positive():
  """Test positive cases for subtract."""
  assert Operations.subtract(5, 3) == 2
  assert Operations.subtract(0, 0) == 0
  assert Operations.subtract(10, 5) == 5

def test_subtract_negative():
  """Test negative cases for subtract."""
  assert Operations.subtract(-5, -3) == -2
  assert Operations.subtract(3, 5) == -2

def test_multiply_positive():
  """Test positive cases for multiply."""
  assert Operations.multiply(2, 3) == 6
  assert Operations.multiply(0, 10) == 0
  assert Operations.multiply(-2, -3) == 6

def test_multiply_negative():
  """Test negative cases for multiply."""
  assert Operations.multiply(2, -3) == -6
  assert Operations.multiply(-2, 3) == -6

def test_divide_positive():
  """Test positive cases for divide."""
  assert Operations.divide(6, 3) == 2
  assert Operations.divide(-6, -3) == 2

def test_divide_negative():
  """Test negative cases for divide."""
  assert Operations.divide(6, -3) == -2
  assert Operations.divide(-6, 3) == -2

def test_divide_by_zero():
  """Test divide by zero."""
  with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
    Operations.divide(1, 0)

def test_power():
  assert Operations.power(2, 3) == 8
  assert Operations.power(3, 2) == 9
  assert Operations.power(5, 0) == 1
  assert Operations.power(2, -1) == 0.5

def test_root():
  assert Operations.root(2, 9) == 3.0
  assert Operations.root(3, 8) == 2.0
  assert Operations.root(2, 4) == 2.0

def test_root_degree_zero_raises():
  with pytest.raises(ValueError, match="Root degree cannot be zero."):
    Operations.root(0, 9)
