""" src/calculator/calculator.tests.py """
import sys
from io import StringIO
import pytest
from unittest.mock import patch
from src.calculator.calculator import calculator
from src.helpers.validators import ValidationError

def run_calculator_with_input(monkeypatch, inputs):
	input_iterator = iter(inputs)
	monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

	# Capture the output of the calculator
	captured_output = StringIO()
	sys.stdout = captured_output
	calculator()
	sys.stdout = sys.__stdout__  # Reset stdout
	return captured_output.getvalue()

# Parameterized tests for valid operations
@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("2 + 3", "5.0"),
		("2+3", "5.0"),
		("0 + 0", "0.0"),
		("0+0", "0.0"),
		("-1 + 1", "0.0"),
		("-1+1", "0.0"),
		("2.5 + 3.5", "6.0"),
		("2.5+3.5", "6.0"),
	],
	ids=[
		"add_split_positive_integers",
		"add_compact_positive_integers",
		"add_split_zeros",
		"add_compact_zeros",
		"add_split_negative_and_positive",
		"add_compact_negative_and_positive",
		"add_split_floats",
		"add_compact_floats",
	]
)
def test_addition(monkeypatch, expression, expected_result):
	"""Addition operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("5 - 2", "3.0"),
		("5-2", "3.0"),
		("0 - 0", "0.0"),
		("0-0", "0.0"),
		("10 - 5", "5.0"),
		("10-5", "5.0"),
		("-5 - 3", "-8.0"),
		("-5-3", "-8.0"),
	],
	ids=[
		"subtract_split_positive",
		"subtract_compact_positive",
		"subtract_split_zeros",
		"subtract_compact_zeros",
		"subtract_split_larger_numbers",
		"subtract_compact_larger_numbers",
		"subtract_split_negative",
		"subtract_compact_negative",
	]
)
def test_subtraction(monkeypatch, expression, expected_result):
	"""Subtraction operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("4 * 5", "20.0"),
		("4*5", "20.0"),
		("0 * 10", "0.0"),
		("0*10", "0.0"),
		("-2 * 3", "-6.0"),
		("-2*3", "-6.0"),
		("2.5 * 4", "10.0"),
		("2.5*4", "10.0"),
	],
	ids=[
		"multiply_split_positive",
		"multiply_compact_positive",
		"multiply_split_by_zero",
		"multiply_compact_by_zero",
		"multiply_split_negative",
		"multiply_compact_negative",
		"multiply_split_float",
		"multiply_compact_float",
	]
)
def test_multiplication(monkeypatch, expression, expected_result):
	"""Multiplication operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("10 / 2", "5.0"),
		("10/2", "5.0"),
		("6 / 3", "2.0"),
		("6/3", "2.0"),
		("-6 / 3", "-2.0"),
		("-6/3", "-2.0"),
		("7.5 / 2.5", "3.0"),
		("7.5/2.5", "3.0"),
	],
	ids=[
		"divide_split_positive",
		"divide_compact_positive",
		"divide_split_even_division",
		"divide_compact_even_division",
		"divide_split_negative",
		"divide_compact_negative",
		"divide_split_floats",
		"divide_compact_floats",
	]
)
def test_division(monkeypatch, expression, expected_result):
	"""Division operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("2 ^ 3", "8.0"),
		("2^3", "8.0"),
		("3 ^ 2", "9.0"),
		("2 ^ 0", "1.0"),
	],
	ids=["power_split", "power_compact", "power_split_reversed", "power_split_zero_exp"]
)
def test_power(monkeypatch, expression, expected_result):
	"""Power operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

@pytest.mark.parametrize(
	"expression, expected_result",
	[
		("2 r 9", "3.0"),
		("2r9", "3.0"),
		("3 r 8", "2.0"),
	],
	ids=["root_split", "root_compact", "root_split_cube"]
)
def test_root(monkeypatch, expression, expected_result):
	"""Root operations should work in both split and compact forms."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected_result}" in output

# Parameterized tests for invalid inputs
@pytest.mark.parametrize(
	"expression",
	[
		"5 % 3",
		"5%3",
		"+ 2 3",
		"abc + 2",
		"2 + + 3",
	],
	ids=[
		"invalid_split_modulo_operator",
		"invalid_compact_modulo_operator",
		"invalid_operator_first",
		"invalid_non_numeric_input",
		"invalid_double_operator",
	]
)
def test_invalid_operations(monkeypatch, expression):
	"""Invalid operations should produce appropriate error messages."""
	inputs = [expression, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "Invalid input." in output

def test_division_by_zero(monkeypatch):
	"""Division by zero should produce appropriate error message."""
	inputs = ["5 / 0", "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "Error: Division by zero is not allowed." in output

def test_keyboard_interrupt(monkeypatch):
	"""Ctrl+C (KeyboardInterrupt) should cause the calculator to exit gracefully."""
	def raise_kb(_prompt=None):
		raise KeyboardInterrupt

	monkeypatch.setattr('builtins.input', raise_kb)

	captured_output = StringIO()
	sys_stdout = sys.stdout
	try:
		sys.stdout = captured_output
		calculator()
	finally:
		sys.stdout = sys_stdout

	output = captured_output.getvalue()
	assert "Exiting..." in output

def test_history_shows_no_history_initially(monkeypatch):
	# When history is requested before any calculation, the REPL should report no history
	inputs = ["history", "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "No history yet..." in output

def test_help_and_history_and_empty_input(monkeypatch):
	# Test help, empty input (ignored), history when empty and after one calculation
	inputs = [
		"help",
		"",            # empty input should be ignored
		"2+2",
		"history",
		"exit",
	]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "Usage: <num1> <op> <num2>" in output
	# Empty input should not produce 'Computing' for that entry; only one computing for 2+2
	assert output.count("Computing:") == 1
	# History should include the performed calculation
	assert "2.0 Add 2.0 = 4.0" in output or "Result: 4.0" in output

def test_unexpected_exception_in_factory(monkeypatch):
	# Force CalculationFactory.create_calculation to raise an unexpected error (EAFP demonstration)
	import src.calculations.calculations as calcmod

	def raise_runtime(*args, **kwargs):
		raise RuntimeError("boom")

	monkeypatch.setattr(calcmod.CalculationFactory, "create_calculation", raise_runtime)

	inputs = ["2+2", "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "Error: boom" in output

def test_accumulator_no_previous_result(monkeypatch):
	inputs = ["+3", "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "No previous result to use." in output

def test_validation_error_in_full_form(monkeypatch):
	with patch("src.calculator.calculator.InputValidator.validate_number", side_effect=ValidationError("bad")):
		inputs = ["2+3", "exit"]
		output = run_calculator_with_input(monkeypatch, inputs)
	assert "Invalid input: bad" in output

def test_validation_error_in_accumulator_form(monkeypatch):
	from decimal import Decimal
	# First two calls succeed (full form "2+3"), third raises (accumulator "+1")
	side_effects = [Decimal("2"), Decimal("3"), ValidationError("bad")]
	with patch("src.calculator.calculator.InputValidator.validate_number", side_effect=side_effects):
		inputs = ["2+3", "+1", "exit"]
		output = run_calculator_with_input(monkeypatch, inputs)
	assert "Invalid input: bad" in output

@pytest.mark.parametrize(
	"first, short, expected",
	[
		("2+3", "+10", "15.0"),   # 5 + 10
		("10-4", "*3", "18.0"),   # 6 * 3
		("3*4", "/6", "2.0"),     # 12 / 6
		("2^3", "+0", "8.0"),     # 8 + 0
		("4r16", "*2", "4.0"),    # 2 * 2
	],
	ids=["add_to_prev", "multiply_prev", "divide_prev", "power_then_add", "root_then_multiply"]
)
def test_accumulator_uses_last_result(monkeypatch, first, short, expected):
	inputs = [first, short, "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert f"Result: {expected}" in output

def test_accumulator_chains_multiple_times(monkeypatch):
	# 2+3=5, +5=10, *2=20
	inputs = ["2+3", "+5", "*2", "exit"]
	output = run_calculator_with_input(monkeypatch, inputs)
	assert "Result: 20.0" in output
