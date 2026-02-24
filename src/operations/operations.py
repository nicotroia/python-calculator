class Operations:
  @staticmethod
  def add(a: float, b: float) -> float:
    return a + b

  @staticmethod
  def subtract(a: float, b: float) -> float:
    return a - b

  @staticmethod
  def multiply(a: float, b: float) -> float:
    return a * b

  @staticmethod
  def divide(a: float, b: float) -> float:
    if b == 0:
      raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

  @staticmethod
  def power(a: float, b: float) -> float:
    return a ** b

  @staticmethod
  def root(a: float, b: float) -> float:
    """Returns the a-th root of b (e.g. root(2, 9) == 3.0)."""
    if a == 0:
      raise ValueError("Root degree cannot be zero.")
    return b ** (1 / a)
