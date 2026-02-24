from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

MAX_INPUT_VALUE = Decimal("1e999")

class ValidationError(ValueError):
    pass

@dataclass
class InputValidator:
    @staticmethod
    def validate_number(value: Any, max_input_value: Decimal = MAX_INPUT_VALUE) -> Decimal:
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {max_input_value}")
            return number.normalize()
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e
