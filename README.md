# Simple REPL Calculator in Python

## Setup

```bash
git clone <url>
cd python-calculator
pip install -r requirements.txt
source .venv/bin/activate
```

## Run the app

```bash
python main.py
```

Then type "exit" or press Cmd+c to quit.

## Supported operations

Supports compact or split inputs — `3 + 2` or `3+2`.

| Operator | Symbol | Example | Result              |
| -------- | ------ | ------- | ------------------- |
| Add      | `+`    | `2 + 3` | `5`                 |
| Subtract | `-`    | `5 - 2` | `3`                 |
| Multiply | `*`    | `4 * 3` | `12`                |
| Divide   | `/`    | `9 / 3` | `3`                 |
| Power    | `^`    | `2 ^ 3` | `8`                 |
| Root     | `r`    | `2 r 9` | `3` (2nd root of 9) |

### Tips

Omit the first number to reuse the last result:

```
2 + 3   → 5
* 4     → 20
```

## Commands

| Command   | Description                                    |
| --------- | ---------------------------------------------- |
| `help`    | Show usage instructions                        |
| `history` | List all calculations from the current session |
| `exit`    | Exit the calculator                            |
| `Cmd+C`   | Exit immediately                               |

## Logs

Each session's calculations are appended to a daily CSV file in the `logs/` folder, named by date (e.g. `logs/2026-02-24.csv`).

## Exit the virtual env

```bash
deactivate
```
