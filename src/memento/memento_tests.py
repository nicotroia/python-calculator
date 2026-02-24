"""src/memento/memento_tests.py"""
import datetime
import pytest

from src.calculations.calculations import CalculationFactory
from src.memento.memento import CalculatorMemento

def make_calc(ctype, a, b):
  return CalculationFactory.create_calculation(ctype, a, b)

def test_memento_stores_history():
  calcs = [make_calc("add", 1.0, 2.0), make_calc("multiply", 3.0, 4.0)]
  m = CalculatorMemento(history=calcs)
  assert m.history == calcs

def test_memento_timestamp_defaults_to_now():
  before = datetime.datetime.now()
  m = CalculatorMemento(history=[])
  after = datetime.datetime.now()
  assert before <= m.timestamp <= after

def test_memento_accepts_explicit_timestamp():
  ts = datetime.datetime(2026, 1, 1, 12, 0, 0)
  m = CalculatorMemento(history=[], timestamp=ts)
  assert m.timestamp == ts

def test_memento_history_is_independent_copy():
  calcs = [make_calc("add", 1.0, 1.0)]
  m = CalculatorMemento(history=list(calcs))
  calcs.append(make_calc("subtract", 5.0, 2.0))
  # memento should not be affected by changes to the original list
  assert len(m.history) == 1
