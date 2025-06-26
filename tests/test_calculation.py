"""This module provides the test suites for the Calculation module at app/calculation"""
import pytest
import logging as log

from decimal import Decimal
from datetime import datetime
from typing import Dict, Any

from app.calculation import Calculation
from app.exceptions import SerializationError

@pytest.mark.parametrize(
        "data, expected",
        [({
            "operation": "add", "operandx": 8, "operandy": 6, "result": 14
        },{ "operation": "add", "operandx": 8, "operandy": 6, "result": 14
        }),({
            "operation": "subtract", "operandx": 14, "operandy": 8, "result": 6
        },{ "operation": "subtract", "operandx": 14, "operandy": 8, "result": 6
        }),({
            "operation": "multiply", "operandx": 6, "operandy": 8, "result": 48
        },{ "operation": "multiply", "operandx": 6, "operandy": 8, "result": 48
        }),({ 
            "operation": "divide", "operandx": 48, "operandy": 8, "result": 6
        },{ "operation": "divide", "operandx": 48, "operandy": 8, "result": 6
        }),({
            "operation": "power", "operandx": 2, "operandy": 3, "result": 8
        },{ "operation": "power", "operandx": 2, "operandy": 3, "result": 8
        }),({
            "operation": "root", "operandx": 8, "operandy": 3, "result": 2
        },{ "operation": "root", "operandx": 8, "operandy": 3, "result": 2
        })],
        ids=[
            "valid_add",
            "valid_subtract",
            "valid_multiply",
            "valid_divide",
            "valid_power",
            "valid_root",
])
def test_from_dict(data: Dict[str, Any], expected: Dict[str, Any]):
    """Tests from_dict with a valid dictionary for each type of operation"""
    data['precision'] = 10
    data['timestamp'] = datetime.now().isoformat()
    calc = Calculation.from_dict(data)
    assert calc.operation == expected['operation'], \
        f"Expected {expected['operation']}, in operation field. Got {calc.operation}" 
    assert calc.operandx == expected['operandx'], \
        f"Expected {expected['operandx']}, in operandx field. Got {calc.operandx}"
    assert calc.operandy == expected['operandy'], \
        f"Expected {expected['operandy']}, in operandy field. Got {calc.operandy}"
    assert calc.result == expected['result'], \
        f"Expected {expected['result']}, in result field. Got {calc.result}"

@pytest.mark.parametrize(
        "data, expected",
        [({
        }, "Error in field deserialization: 'operation'"
        ),({
            "operation": 17.5, "operandx": 8, "operandy": 6, "result": 14
        }, "Error in field deserialization: 'float' object has no attribute 'lower'"
        ),({
            "operation": "add", "operandx": 8, "operandy": 6, "result": "fourteen"
        }, "Error in field deserialization: Invalid data passed to Decimal()"
        ),({
            "operation": "nonsense", "operandx": 1, "operandy": 1, "result": 0
        }, "Data record contains an invalid operation tag"
        ),({
            "operation": "divide", "operandx": 2, "operandy": 0, "result": 0
        }, "Data record contains invalid operands: Divisor operand cannot be 0"
        ),({
            "operation": "root", "operandx": 2, "operandy": 0, "result": 0
        }, "Data record contains invalid operands: Zero radicand is undefined"
        )],
        ids=[
            "missing_data",
            "bad_value_type",
            "bad_decimal_value",
            "bad_op_tag",
            "zero_divisor_calc",
            "zero_radicand_calc",
])
def test_err_from_dict(data: Dict[str, Any], expected: str):
    """Tests error handling on the from_dict method"""
    with pytest.raises(SerializationError) as exc_info:
        data['precision'] = 10
        data['timestamp'] = datetime.now().isoformat()
        calc = Calculation.from_dict(data)
    assert str(exc_info.value) == expected, \
        f"Expected error message '{exc_info.value}'. Got '{expected}'"

def test_bad_result_from_dict(caplog):
    """Tests the warning log launched by from_dict where result is invalid"""
    caplog.set_level(log.WARNING)
    calc_dict = {"operation": "add", "operandx": 2, "operandy": 2, "result": 5}
    calc_dict['precision'] = 10
    calc_dict['timestamp'] = datetime.now().isoformat()
    calc = Calculation.from_dict(calc_dict)
    assert f"Loaded calculation result {calc_dict['result']}" in caplog.text
    assert f"differs from computed result 4" in caplog.text

def test_to_dict():
    """Tests the to_dict method"""
    calc = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    assert calc.to_dict() == {
        "operation": "add",
        "operandx": Decimal(8),
        "operandy": Decimal(6),
        "result": Decimal(14),
        "precision": calc.precision,
        "timestamp": calc.timestamp.isoformat()
    }

def test_to_str():
    """Tests the __str__ method"""
    calc = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    assert calc.__str__() == "add(8, 6) = 14"

def test_repr():
    """Tests the __repr__ method"""
    calc = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    assert calc.__repr__() == (
        "Calculation(operation='add', operandx = 8, operandy = 6, result = 14, "
        f"precision = {calc.precision}, "
        f"timestamp = '{calc.timestamp.isoformat()}')"
    )

def test_valid_eq():
    calc = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    other = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    assert calc.__eq__(other)

@pytest.mark.parametrize(
        "other",
        [
            datetime.now(),
            Calculation(operation="subtract", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14")),
            Calculation(operation="add", operandx=Decimal("7"), operandy=Decimal("6"), result=Decimal("14")),
            Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("7"), result=Decimal("14")),
            Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("77"))
        ],
        ids=[
            "bad_type",
            "bad_op",
            "bad_x",
            "bad_y",
            "bad_result"
])
def test_bad_eq(other: object):
    calc = Calculation(operation="add", operandx=Decimal("8"), operandy=Decimal("6"), result=Decimal("14"))
    assert not calc.__eq__(other), f"Object <{other.__repr__}> flagged as equal to <{calc.__repr__}>"
