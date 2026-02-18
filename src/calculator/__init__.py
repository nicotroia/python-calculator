
import re

from src.calculations import CalculationFactory


def calculator():
  """Basic REPL calculator that performs addition, subtraction, multiplication, and division.

  Accepts either spaced input like: 2 + 2
  Or compact input like: 2+2
  Ctrl+C will exit the program.
  Special commands: 'help', 'history', 'exit'
  """

  print("Welcome to Nico's calculator! Enter an expression or type 'exit' to quit")
  print("(ie. '2+2', '5-2', '3/4', '8*2')")

  op_to_type = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
  }

  # Keep a log of calculations performed in this session
  history = []

  while True:
    try:
      user_input = input("Enter an expression: ")

    except KeyboardInterrupt:
      print("\nExiting...")
      return

    if not user_input:
      continue

    cmd = user_input.strip().lower()
    if cmd == "exit":
      print("Exiting...")
      break
    if cmd == "help":
      print("Usage: <num1> <op> <num2> where op is one of + - * /\nSpecial commands: help, history, exit")
      continue
    if cmd == "history":
      if not history:
        print("No history yet...")
      else:
        for item in history:
          print(str(item))
      continue

    s = user_input.strip()

    # Parse input with regex: '<num1><op><num2>'
    m = re.match(r'^([+-]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\d+(?:\.\d+)?)$', s)
    if not m:
      print("Invalid input. Please use the format: <num1> <operation> <num2>. Supported operations: + - * /")
      continue

    num1, num2 = float(m.group(1)), float(m.group(3))
    operation = m.group(2)

    print(f"Computing: {num1} {operation} {num2}")

    try:
      calc_type = op_to_type[operation]
      calc = CalculationFactory.create_calculation(calc_type, num1, num2)
      result = calc.execute()
    except ZeroDivisionError as e:
      print(f"Error: {e}")
      continue
    except Exception as e:
      print(f"Error: {e}")
      continue

    history.append(calc)
    print(f"Result: {result}")
