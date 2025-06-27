import os
import pytest
from decimal import Decimal
from typing import Any

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator

@pytest.mark.parametrize(
        "value, expected",
        [
            (100, Decimal('100')),
            (-100, Decimal('-100')),
            (100.001, Decimal('100.001')),
            (-100.001, Decimal('-100.001')),
            ("100", Decimal('100')),
            ("100.001", Decimal('100.001')),
            ("-100", Decimal('-100')),
            ("-100.001", Decimal('-100.001')),
            (0, Decimal('0')),
            ("  100  ", Decimal('100')),
        ],
        ids=[
            "positive_int",
            "negative_int",
            "positive_float",
            "negative_float",
            "positive_string",
            "positive_string_decimal",
            "negative_string",
            "negative_string_decimal",
            "zero_val",
            "whitespaced_val"
])
def test_valid_inputs(value: Any, expected: Decimal):
    """Tests a range of valid input for their Decimal conversions"""
    decimal = InputValidator.validate_number(value)
    assert decimal == expected, \
    f"Expected {expected} from {value}. Got {decimal}"

@pytest.mark.parametrize(
        "value, expected",
        [
            ("nonsense", "Invalid number format: nonsense"),
            ("", "Invalid number format: "),
            ("\t", "Invalid number format: "),
            (None, "Invalid number format: None"),
            ([], "Invalid number format: "),
            (1001, "Value exceeds allowed maximum: 1000"),
            (-1001, "Value exceeds allowed maximum: 1000"),
            ("1001", "Value exceeds allowed maximum: 1000"),

        ],
        ids=[
            "bad_string",
            "empty_val",
            "whitespace_val",
            "NoneType_val",
            "bad_type",
            "overflow_positive",
            "overflow_negative",
            "overflow_string",
])
def test_bad_inputs(value: Any, expected: str):
    """Tests error handling for invalid inputs in validate_number"""
    os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
    with pytest.raises(ValidationError, match=expected):
        InputValidator.validate_number(value)
    os.environ.pop('CALCULATOR_MAX_INPUT_VALUE')
    CalculatorConfig._instance = None

