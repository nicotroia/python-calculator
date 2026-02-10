
import re

from src.helpers.operations import Operations

def calculator():
  """Basic REPL calculator that performs addition, subtraction, multiplication, and division.

  Accepts either spaced input like: 2 + 2
  Or compact input like: 2+2
  Ctrl+C will exit the program.
  """

  print("Welcome to Nico's calculator! Enter an expression or type 'exit' to quit")
  print("(ie. '2+2', '5-2', '3/4', '8*2')")

  operations_map = {
    '+': Operations.add,
    '-': Operations.subtract,
    '*': Operations.multiply,
    '/': Operations.divide
  }

  while True:
    try:
      user_input = input(
        "Enter an expression: "
      )

    except KeyboardInterrupt:
      print("\nExiting...")
      return

    if user_input.lower() == "exit":
      print("Exiting...")
      break

    s = user_input.strip()

    # Parse input with regex: '<num1><op><num2>'
    parsed = False
    m = re.match(r'^([+-]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\d+(?:\.\d+)?)$', s)
    if m:
      num1, num2 = float(m.group(1)), float(m.group(3))
      operation = m.group(2)
      parsed = True

    # Cannot parse input
    if not parsed:
      print("Invalid input. Please use the format: <num1> <operation> <num2>. Supported operations: + - * /")
      continue

    print(f"Computing: {num1} {operation} {num2}")

    # Compute results using map of operations
    try:
      result = operations_map[operation](num1, num2)
    except ValueError as e:
      print(f"Error: {e}")
      continue

    print(f"Result: {result}")
