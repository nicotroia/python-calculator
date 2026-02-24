"""src/helpers/calculation_record_tests.py"""
import datetime
import pytest

from src.calculations.calculations import CalculationFactory
from src.helpers.calculation_record import CalculationRecord

def test_record_stores_calculation_and_timestamp():
  calc = CalculationFactory.create_calculation("add", 2.0, 3.0)
  record = CalculationRecord(calculation=calc)
  assert record.calculation is calc
  assert isinstance(record.timestamp, datetime.datetime)

def test_record_accepts_explicit_timestamp():
  calc = CalculationFactory.create_calculation("multiply", 3.0, 4.0)
  ts = datetime.datetime(2026, 2, 24, 12, 0, 0)
  record = CalculationRecord(calculation=calc, timestamp=ts)
  assert record.timestamp == ts

def test_record_str_includes_timestamp_and_calculation():
  calc = CalculationFactory.create_calculation("add", 2.0, 3.0)
  ts = datetime.datetime(2026, 2, 24, 12, 0, 0)
  record = CalculationRecord(calculation=calc, timestamp=ts)
  assert str(record) == "2026-02-24 12:00:00: 2.0 Add 3.0 = 5.0"
