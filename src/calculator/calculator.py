import re
import datetime
import logging

from src.calculations.calculations import CalculationFactory
from src.history.history import LoggingObserver, CsvLoggingObserver

def calculator():
  """Basic REPL calculator that performs addition, subtraction, multiplication, division, power, and root.
  Accepts either spaced input like: 2 + 2
  Or compact input like: 2+2
  Use ^ for power (2^3 = 8) and r for root (2r9 = 3, i.e. 2nd root of 9).
  Accumulator: omit the first number to reuse the last result (e.g. '+3', '*2').
  Ctrl+C will exit the program.
  Special commands: 'help', 'history', 'exit'
  """

  print("Welcome to Nico's calculator! Enter an expression or type 'exit' to quit")
  print("(ie. '2+2', '5-2', '3/4', '8*2', '2^3', '2r9')")

  op_to_type = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
    '^': 'power',
    'r': 'root',
  }

  # Keep a log of calculations performed in this session
  observers = [LoggingObserver(), CsvLoggingObserver()]
  history: list[tuple[str, object]] = []
  last_result: float | None = None

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
      print("Usage: <num1> <op> <num2> where op is one of: [+ - * / ^ r]\n"
            "Accumulator: omit <num1> to reuse the last result (e.g. '+3')\n"
            "Special commands: help, history, exit")
      continue
    if cmd == "history":
      if not history:
        print("No history yet...")
      else:
        for ts, item in history:
          print(f"{ts}: {item}")
      continue

    s = user_input.strip()

    # Full form: '<num1> <op> <num2>'
    m = re.match(r'^([+-]?\d+(?:\.\d+)?)\s*([+\-*/^r])\s*([+-]?\d+(?:\.\d+)?)$', s)
    if m:
      num1, num2 = float(m.group(1)), float(m.group(3))
      operation = m.group(2)
    else:
      # Accumulator form: '<op> <num2>' — reuses last result as num1
      m2 = re.match(r'^([+\-*/^r])\s*([+-]?\d+(?:\.\d+)?)$', s)
      if not m2:
        print("Invalid input. Please use the format: <num1> <operation> <num2>. Supported operations: + - * / ^ r")
        continue
      if last_result is None:
        print("No previous result to use. Please enter a full expression first.")
        continue
      operation = m2.group(1)
      num1, num2 = last_result, float(m2.group(2))

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

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history.append((ts, calc))
    last_result = result
    for obs in observers:
      obs.update(calc)
    print(f"Result: {result}")
