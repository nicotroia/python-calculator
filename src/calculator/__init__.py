
import re

from src.helpers import add, subtract, multiply, divide

def calculator():
  """Basic REPL calculator that performs addition, subtraction, multiplication, and division.

  Accepts either spaced input like: 2 + 2
  Or compact input like: 2+2
  Ctrl+C will exit the program.
  """

  print("Welcome to Nico's calculator! Enter an expression or type 'exit' to quit")
  print("(ie. '2+2', '5-2', '3/4', '8*2')")

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

    # Try split form first: '<num1> <op> <num2>'
    parsed = False
    parts = s.split()
    if len(parts) == 3:
      num1_s, operation, num2_s = parts
      # Only accept four basic operators
      if operation in ('+', '-', '*', '/'):
        num1, num2 = float(num1_s), float(num2_s)
        parsed = True
    # Try compact form: '<num1><op><num2>'
    else:
      m = re.match(r'^([+-]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\d+(?:\.\d+)?)$', s)
      if m:
        num1, num2 = float(m.group(1)), float(m.group(3))
        operation = m.group(2)
        parsed = True

    if not parsed:
      print("Invalid input. Please use the format: <num1> <operation> <num2>. Supported operations: + - * /")
      continue

    print(f"Computing: {num1} {operation} {num2}")

    # Compute results
    if operation == "+":
      result = add(num1, num2)
    elif operation == "-":
      result = subtract(num1, num2)
    elif operation == "*":
      result = multiply(num1, num2)
    else:
      if num2 == 0:
        print("Error: division by zero")
        continue
      result = divide(num1, num2)

    print(f"Result: {result}")
