from abc import ABC, abstractmethod
import datetime
import logging
from pathlib import Path
from typing import Protocol

import pandas as pd

from src.calculations.calculations import Calculation

_DEFAULT_LOG_DIR = Path(__file__).parents[2] / "logs"

class CalculatorConfig(Protocol):
  auto_save: bool

class CalculatorProtocol(Protocol):
  config: CalculatorConfig
  def save_history(self) -> None: ...  # pragma: no cover

class HistoryObserver(ABC):
  @abstractmethod
  def update(self, calculation: Calculation) -> None:
    pass  # pragma: no cover

class LoggingObserver(HistoryObserver):
  def update(self, calculation: Calculation) -> None:
    if calculation is None:
      raise AttributeError("Calculation cannot be None")
    logging.info(f"Calculation performed: {calculation}")

class AutoSaveObserver(HistoryObserver):
  def __init__(self, calculator: CalculatorProtocol):
    if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
      raise TypeError("Calculator must have 'config' and 'save_history' attributes")
    self.calculator = calculator

  def update(self, calculation: Calculation) -> None:
    if calculation is None:
      raise AttributeError("Calculation cannot be None")
    if self.calculator.config.auto_save:
      self.calculator.save_history()
      logging.info("History auto-saved")

class CsvLoggingObserver(HistoryObserver):
  _COLUMNS = ["timestamp", "operation", "a", "b", "result"]

  def __init__(self, log_dir: Path = _DEFAULT_LOG_DIR):
    log_dir.mkdir(parents=True, exist_ok=True)
    self.csv_path = log_dir / f"{datetime.date.today()}.csv"
    if not self.csv_path.exists():
      pd.DataFrame(columns=self._COLUMNS).to_csv(self.csv_path, index=False)

  def update(self, calculation: Calculation) -> None:
    if calculation is None:
      raise AttributeError("Calculation cannot be None")
    row = pd.DataFrame([{
      "timestamp": datetime.datetime.now().isoformat(),
      "operation": calculation.__class__.__name__.replace("Calculation", ""),
      "a": calculation.a,
      "b": calculation.b,
      "result": calculation.execute(),
    }])
    row.to_csv(self.csv_path, mode="a", header=False, index=False)
