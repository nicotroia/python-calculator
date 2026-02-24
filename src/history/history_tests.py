"""src/history/history_tests.py"""
import datetime
import logging
import pytest
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd

from src.calculations.calculations import CalculationFactory
from src.history.history import HistoryObserver, LoggingObserver, AutoSaveObserver, CsvLoggingObserver


def test_history_observer_is_abstract():
  with pytest.raises(TypeError):
    HistoryObserver()  # type: ignore


def test_logging_observer_logs_calculation(caplog):
  calc = CalculationFactory.create_calculation("add", 2.0, 3.0)
  observer = LoggingObserver()
  with caplog.at_level(logging.INFO):
    observer.update(calc)
  assert "2.0 Add 3.0 = 5.0" in caplog.text


def test_logging_observer_raises_on_none():
  observer = LoggingObserver()
  with pytest.raises(AttributeError, match="Calculation cannot be None"):
    observer.update(None)  # type: ignore


def test_auto_save_observer_raises_on_invalid_calculator():
  with pytest.raises(TypeError, match="Calculator must have"):
    AutoSaveObserver(object())


def test_auto_save_observer_saves_when_enabled():
  calc = CalculationFactory.create_calculation("add", 1.0, 1.0)
  mock_calculator = MagicMock()
  mock_calculator.config.auto_save = True
  observer = AutoSaveObserver(mock_calculator)
  observer.update(calc)
  mock_calculator.save_history.assert_called_once()


def test_auto_save_observer_skips_save_when_disabled():
  calc = CalculationFactory.create_calculation("add", 1.0, 1.0)
  mock_calculator = MagicMock()
  mock_calculator.config.auto_save = False
  observer = AutoSaveObserver(mock_calculator)
  observer.update(calc)
  mock_calculator.save_history.assert_not_called()


def test_auto_save_observer_raises_on_none():
  mock_calculator = MagicMock()
  observer = AutoSaveObserver(mock_calculator)
  with pytest.raises(AttributeError, match="Calculation cannot be None"):
    observer.update(None)  # type: ignore


def test_csv_observer_creates_csv_on_init(tmp_path):
  CsvLoggingObserver(log_dir=tmp_path)
  today = datetime.date.today()
  csv_file = tmp_path / f"{today}.csv"
  assert csv_file.exists()
  df = pd.read_csv(csv_file)
  assert list(df.columns) == ["timestamp", "operation", "a", "b", "result"]
  assert len(df) == 0


def test_csv_observer_appends_row_on_update(tmp_path):
  calc = CalculationFactory.create_calculation("add", 2.0, 3.0)
  observer = CsvLoggingObserver(log_dir=tmp_path)
  observer.update(calc)
  df = pd.read_csv(tmp_path / f"{datetime.date.today()}.csv")
  assert len(df) == 1
  assert df.iloc[0]["operation"] == "Add"
  assert df.iloc[0]["a"] == 2.0
  assert df.iloc[0]["b"] == 3.0
  assert df.iloc[0]["result"] == 5.0


def test_csv_observer_appends_multiple_rows(tmp_path):
  observer = CsvLoggingObserver(log_dir=tmp_path)
  observer.update(CalculationFactory.create_calculation("add", 1.0, 1.0))
  observer.update(CalculationFactory.create_calculation("multiply", 3.0, 4.0))
  df = pd.read_csv(tmp_path / f"{datetime.date.today()}.csv")
  assert len(df) == 2


def test_csv_observer_does_not_overwrite_existing_csv(tmp_path):
  # Pre-create a CSV with one row
  observer = CsvLoggingObserver(log_dir=tmp_path)
  observer.update(CalculationFactory.create_calculation("add", 1.0, 1.0))
  # Re-initialising with the same dir should not wipe the existing file
  CsvLoggingObserver(log_dir=tmp_path)
  df = pd.read_csv(tmp_path / f"{datetime.date.today()}.csv")
  assert len(df) == 1


def test_csv_observer_raises_on_none(tmp_path):
  observer = CsvLoggingObserver(log_dir=tmp_path)
  with pytest.raises(AttributeError, match="Calculation cannot be None"):
    observer.update(None)  # type: ignore
