from abc import ABC, abstractmethod

from src.operations import Operations

class Calculation(ABC):
  def __init__(self, a: float, b: float) -> None:
    self.a: float = a
    self.b: float = b

  @abstractmethod
  def execute(self) -> float:
    pass # pragma: no cover

  def __str__(self) -> str:
    """
    Provides a user-friendly string representation of the Calculation instance.
    
    **Returns:**
    - `str`: A string describing the calculation and its result.
    """
    result = self.execute()
    operation_name = self.__class__.__name__.replace('Calculation', '')
    return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"

  def __repr__(self) -> str:
    """
    Provides a technical, unambiguous representation of the Calculation instance 
    showing the class name and operand values.

    **Returns:**
    - `str`: A string containing the class name and operands.
    """
    return f"{self.__class__.__name__}(a={self.a}, b={self.b})"

class CalculationFactory:
  # _calculations is a dictionary that holds a mapping of calculation types 
  _calculations = {}

  @classmethod
  def register_calculation(cls, calculation_type: str):
    def decorator(subclass):
      # Lowercase the type to ensure consistency
      calculation_type_lower = calculation_type.lower()
      # Check if the calculation type has already been registered
      if calculation_type_lower in cls._calculations:
        raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
      # Register the subclass
      cls._calculations[calculation_type_lower] = subclass
      return subclass
    return decorator

  @classmethod
  def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
    calculation_type_lower = calculation_type.lower()
    calculation_class = cls._calculations.get(calculation_type_lower)
    # If the type is unsupported, raise an error with the available types.
    if not calculation_class:
      available_types = ', '.join(cls._calculations.keys())
      raise ValueError(f"Unsupported calculation type: '{calculation_type}'. Available types: {available_types}")
    # Create and return an instance of the requested calculation class with the provided operands.
    return calculation_class(a, b)

# Concrete Calculation Classes
# Each of these classes defines a specific calculation type
@CalculationFactory.register_calculation('add')
class AddCalculation(Calculation):
  def execute(self) -> float:
    return Operations.add(self.a, self.b)

@CalculationFactory.register_calculation('subtract')
class SubtractCalculation(Calculation):
  def execute(self) -> float:
    return Operations.subtract(self.a, self.b)

@CalculationFactory.register_calculation('multiply')
class MultiplyCalculation(Calculation):
  def execute(self) -> float:
    return Operations.multiply(self.a, self.b)

@CalculationFactory.register_calculation('divide')
class DivideCalculation(Calculation):
  def execute(self) -> float:
    return Operations.divide(self.a, self.b)
