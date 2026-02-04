def add(a: float, b: float) -> float:
  return a + b

def subtract(a: float, b: float) -> float:
  return a - b

def multiply(a: float, b: float) -> float:
  return a * b

def divide(a: float, b: float) -> float:
  if b == 0:
    raise ValueError("Division by zero is not allowed.")  # This sends an error message when someone tries to divide by zero.
  
  return a / b
