from dataclasses import dataclass, field
import datetime
from typing import List

from src.calculations.calculations import Calculation

@dataclass
class CalculatorMemento:
  history: List[Calculation]
  timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
