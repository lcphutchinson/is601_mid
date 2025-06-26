import pytest

from datetime import datetime

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento

def test_from_dict():
    """Tests the from_dict method"""
    inputs = { "history": [{
        "operation": "add",
        "operandx": 8,
        "operandy": 6,
        "result": 14,
        "precision": 10,
        "timestamp": datetime.now().isoformat()
    }],
        "timestamp": datetime.now().isoformat()
    }
    mem = CalculatorMemento.from_dict(inputs)
    assert all([
        mem.history[0].operation == "add",
        mem.history[0].operandx == 8,
        mem.history[0].operandy == 6,
        mem.history[0].result == 14
        ]), f"History record does not match dict base"

def test_to_dict():
    """Tests the to_dict method"""
    calc = Calculation(operation="add", operandx=8, operandy=6, result=14)
    mem = CalculatorMemento(history=[calc])
    assert mem.to_dict() == {
        "history": [{
            "operation": "add",
            "operandx": 8,
            "operandy": 6,
            "result": 14,
            "precision": mem.history[0].precision,
            "timestamp": mem.history[0].timestamp.isoformat()
        }],
        "timestamp": mem.timestamp.isoformat()
        }, f"History dict does not match record base"
