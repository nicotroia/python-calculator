""" tests/test_calculator.py """
import sys
from io import StringIO
from src.calculator import calculator

def run_calculator_with_input(monkeypatch, inputs):
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()

# Positive Tests
def test_addition_split(monkeypatch):
    """Test addition operation in split form:"""
    inputs = ["2 + 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_addition_compact(monkeypatch):
    """Test addition operation in compact form:"""
    inputs = ["2+3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_subtraction_split(monkeypatch):
    """Test subtraction operation in split form:"""
    inputs = ["5 - 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output

def test_subtraction_compact(monkeypatch):
    """Test subtraction operation in compact form:"""
    inputs = ["5-2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output

def test_multiplication_split(monkeypatch):
    """Test multiplication operation:"""
    inputs = ["4 * 5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 20.0" in output

def test_multiplication_compact(monkeypatch):
    """Test multiplication operation in compact form:"""
    inputs = ["4*5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 20.0" in output

def test_division_split(monkeypatch):
    """Test division operation in split form:"""
    inputs = ["10 / 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

def test_division_compact(monkeypatch):
    """Test division operation in compact form:"""
    inputs = ["10/2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

# Negative Tests
def test_invalid_operation(monkeypatch):
    """Test invalid operation:"""
    inputs = ["5 % 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input." in output

def test_invalid_input_format(monkeypatch):
    """Test invalid input format:"""
    inputs = ["+ 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input." in output

def test_division_by_zero(monkeypatch):
    """Test division by zero:"""
    inputs = ["5 / 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Error: division by zero" in output
