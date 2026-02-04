""" tests/test_helpers.py """
import pytest
from src.helpers import add, subtract, multiply, divide

def test_add_positive():
  """Test positive cases for add."""
  assert add(2, 3) == 5
  assert add(0, 0) == 0
  assert add(-1, 1) == 0

def test_add_negative():
  """Test negative cases for add."""
  assert add(-2, -3) == -5
  assert add(-1, 0) == -1

def test_subtract_positive():
  """Test positive cases for subtract."""
  assert subtract(5, 3) == 2
  assert subtract(0, 0) == 0
  assert subtract(10, 5) == 5

def test_subtract_negative():
  """Test negative cases for subtract."""
  assert subtract(-5, -3) == -2
  assert subtract(3, 5) == -2

def test_multiply_positive():
  """Test positive cases for multiply."""
  assert multiply(2, 3) == 6
  assert multiply(0, 10) == 0
  assert multiply(-2, -3) == 6

def test_multiply_negative():
  """Test negative cases for multiply."""
  assert multiply(2, -3) == -6
  assert multiply(-2, 3) == -6

def test_divide_positive():
  """Test positive cases for divide."""
  assert divide(6, 3) == 2
  assert divide(-6, -3) == 2

def test_divide_negative():
  """Test negative cases for divide."""
  assert divide(6, -3) == -2
  assert divide(-6, 3) == -2

def test_divide_by_zero():
  """Test divide by zero."""
  with pytest.raises(ValueError, match="Division by zero is not allowed."):
    divide(1, 0)
