from dataclasses import dataclass, field
import datetime

from src.calculations.calculations import Calculation


@dataclass
class CalculationRecord:
  calculation: Calculation
  timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

  def __str__(self) -> str:
    return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {self.calculation}"
