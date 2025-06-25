"""This module defines the test suites for classes in the Operations module at app/Operations"""
import pytest
from decimal import Decimal
from typing import Any, Dict, Type

import app.exceptions as exc
import app.operations as ops

class TestBaseOperation:
    """Defines the test suite for Operation base class methods"""

    def test_str_representation(self):
        """Test the string representation of a child Operation class"""
        class TestOperation(ops.Operation):
            def execute(self, x: Decimal, y: Decimal) -> Decimal:
                return x

        assert str(TestOperation()) == "TestOperation"

class BaseOperationTest:
    """Base class for tests on the Operation class family"""
    operation_class: Type[ops.Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Runs tests on the valid test case set, representing valid inputs"""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            x = Decimal(str(case["x"]))
            y = Decimal(str(case["y"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(x, y)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Runs tests on the invalid test case set, representing error-causing inputs"""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            x = Decimal(str(case["x"]))
            y = Decimal(str(case["y"]))
            error = case.get("error", exc.ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(x, y)

class TestAddition(BaseOperationTest):
    """Defines the test suite for the Addition Operation"""
    operation_class = ops.Addition
    valid_test_cases = {
            "positive_operands": {"x": "1", "y": "2", "expected": "3"},
            "mixed_operands_pos": {"x": "-1", "y": "2", "expected": "1"},
            "mixed_operands_neg": {"x": "1", "y": "-2", "expected": "-1"},
            "negative_operands": {"x": "-1", "y": "-2", "expected": "-3"},
            "zero_sum": {"x": "1", "y": "-1", "expected": "0"},
            "positive_floats": {"x": "1.5", "y": "2.5", "expected": "4"},
            "mixed_floats": {"x": "-1.5", "y": "2.5", "expected": "1"},
            "negative_floats": {"x": "1", "y": "2", "expected": "3"},
            "large_operands": {"x": "-1e10", "y": "2e10", "expected": "1e10"},
    }
    invalid_test_cases = {}

class TestSubtraction(BaseOperationTest):
    """Defines the test suite for the Subtraction Operation"""
    operation_class = ops.Subtraction
    valid_test_cases = {
            "large_base_pos": {"x": "3", "y": "2", "expected": "1"},
            "small_base_pos": {"x": "2", "y": "3", "expected": "-1"},
            "large_base_neg": {"x": "-3", "y": "-2", "expected": "-1"},
            "small_base_neg": {"x": "-2", "y": "-3", "expected": "1"},
            "mixed_operands": {"x": "1", "y": "-2", "expected": "3"},
            "zero_diff": {"x": "2", "y": "2", "expected": "0"},
            "positive_floats": {"x": "3.5", "y": "2.5", "expected": "1"},
            "negative_floats": {"x": "-3.5", "y": "-2.5", "expected": "-1"},
            "large_operands": {"x": "2e10", "y": "1e10", "expected": "1e10"},
    }
    invalid_test_cases = {}

class TestMultiplication(BaseOperationTest):
    """Defines the test suite for the Multiplication Operation"""
    operation_class = ops.Multiplication
    valid_test_cases = {
            "positive_operands": {"x": "2", "y": "4", "expected": "8"},
            "mixed_operands": {"x": "2", "y": "-4", "expected": "-8"},
            "negative_operands": {"x": "-2", "y": "-4", "expected": "8"},
            "zero_operand": {"x": "8", "y": "0", "expected": "0"},
            "positive_floats": {"x": "2.0", "y": "4.0", "expected": "8.0"},
            "mixed_floats": {"x": "2.5", "y": "-2.0", "expected": "-5.0"},
            "negative_floats": {"x": "-2.5", "y": "-2.0", "expected": "5.0"},
            "fractional_float": {"x": "8.0", "y": "0.5", "expected": "4.0"},
            "large_operand": {"x": "1e10", "y": "2", "expected": "2e10"},
    }
    invalid_test_cases = {}

class TestDivision(BaseOperationTest):
    """Defines the test suite for the Division Operation"""
    operation_class = ops.Division
    valid_test_cases = {
            "positive_operands": {"x": "8", "y": "4", "expected": "2"},
            "mixed_operands": {"x": "8", "y": "-4", "expected": "-2"},
            "negative_operands": {"x": "-8", "y": "-4", "expected": "2"},
            "float_quotient": {"x": "5", "y": "2", "expected": "2.5"},
            "float_divisor": {"x": "2", "y": "0.5", "expected": "4.0"},
            "float_operands": {"x": "8.0", "y": "4.0", "expected": "2.0"},
            "zero_dividend": {"x": "0", "y": "2", "expected": "0"},
    }
    invalid_test_cases = {
            "zero_divisor": {
                "x": "2",
                "y": "0",
                "error": exc.ValidationError,
                "message": "Divisor operand cannot be 0",
            },
    }

class TestPower(BaseOperationTest):
    """Defines the test suite for the Power Operation"""
    operation_class = ops.Power
    valid_test_cases = {
            "positive_operands": {"x": "2", "y": "3", "expected": "8"},
            "negative_square": {"x": "-2", "y": "2", "expected": "4"},
            "negative_cube": {"x": "-2", "y": "3", "expected": "-8"},
            "identity": {"x": "2", "y": "1", "expected": "2"},
            "zero_exponent": {"x": "2", "y": "0", "expected": "1"},
            "negative_exponent": {"x": "2", "y": "-2", "expected": "0.25"},
            "fractional_base": {"x": "0.5", "y": "2", "expected": "0.25"},
            "fractional_exponent": {"x": "4", "y": "0.5", "expected": "2"},
            "zero_base": {"x": "0", "y": "3", "expected": "0"},
    }
    invalid_test_cases = {}

class TestRoot(BaseOperationTest):
    """Defines the test suite for the Root Operation"""
    operation_class = ops.Root
    valid_test_cases = {
            "positive_root": {"x": "4", "y": "2", "expected": "2"},
            "fracitonal_root": {"x": "4", "y": "0.5", "expected": "16"},
            "negative_root": {"x": "4", "y": "-2", "expected": "0.5"},
            "negative_base_odd_root": {"x": "-8", "y": "3", "expected": "-2"},
            "fractional_base": {"x": "0.25", "y": "2", "expected": "0.5"},
            "zero_base": {"x": "0", "y": "2", "expected": "0"},
    }
    invalid_test_cases = {
            "negative_base_even_root": {
                "x": "-4", 
                "y": "2",
                "error": exc.ValidationError,
                "message": "Imaginary roots not supported",
            },
            "zero_root": {
                "x": "2",
                "y": "0",
                "error": exc.ValidationError,
                "message": "Zero radicand is undefined",
            }
    }

class TestModulus(BaseOperationTest):
    """Defines the test suite for the Modulus Operation"""
    operation_class = ops.Modulus
    valid_test_cases = {
            "trivial_mod": {"x": "2", "y": "3", "expected": "2"},
            "positive_mod": {"x": "3", "y": "2", "expected": "1"},
            "negative_dividend": {"x": "-3", "y": "2", "expected": "-1"},
            "negative_divisor": {"x": "3", "y": "-2", "expected": "1"},
            "negative_operands": {"x": "-3", "y": "-2", "expected": "-1"},
            "zero dividend": {"x": "0", "y": "2", "expected": "0"},
            "float_dividend": {"x": "3.5", "y": "2", "expected": "1.5"},
            "float_divisor": {"x": "3", "y": "2.5", "expected": "0.5"}
    }
    invalid_test_cases = {
            "zero_divisor": {
                "x": "3",
                "y": "0",
                "error": exc.ValidationError,
                "message": "Divisor operand cannot be 0"
            }
    }

class Test_Int_Division(BaseOperationTest):
    """Defines the test suite for the Integer Division Operation"""
    operation_class = ops.IntegerDivision
    valid_test_cases = {
            "trivial_int_divide": {"x": "4", "y": "2", "expected": "2"},
            "positive_int_divide": {"x": "5", "y": "2", "expected": "2"},
            "negative_dividend_int_divide": {"x": "-5", "y": "2", "expected": "-2"},
            "negative_divisor_int_divide": {"x": "5", "y": "-2", "expected": "-2"},
            "negative_int_divide": {"x": "-5", "y": "-2", "expected": "2"},
            "zero_divisor_int_divide": {"x": "0", "y": "2", "expected": "0"}
    }
    invalid_test_cases = {
            "zero_divisor": {
                "x": "3",
                "y": "0",
                "error": exc.ValidationError,
                "message": "Divisor operand cannot be 0"
    }
}

class TestPercentage(BaseOperationTest):
    """Defines the test suite for the Percentage Operation"""
    operation_class = ops.Percentage
    valid_test_cases = {
            "positive_percentage": {"x": "2", "y": "4", "expected": "50"},
            "mixed_percentage_x": {"x": "-2", "y": "4", "expected": "-50"},
            "mixed_percentage_y": {"x": "2", "y": "-4", "expected": "-50"},
            "negative_percentage": {"x": "-2", "y": "-4", "expected": "50"},
            "large_percentage": {"x": "4", "y": "2", "expected": "200"},
            "zero_percentage": {"x": "0", "y": "2", "expected": "0"},
            "float_percentage": {"x": "1", "y": "8", "expected": "12.5"},
    }
    invalid_test_cases = {
            "zero_divisor": {
                "x": "3",
                "y": "0",
                "error": exc.ValidationError,
                "message": "Divisor operand cannot be 0"
            }
    }

class TestDistance(BaseOperationTest):
    """Defines the test suite for the Distance Operation"""
    operation_class = ops.Distance
    valid_test_cases = {
            "positive_distance": {"x": "4", "y": "2", "expected": "2"},
            "negative_distance": {"x": "2", "y": "4", "expected": "2"},
            "compound_distance": {"x": "-2", "y": "4", "expected": "6"},
            "zero_distance": {"x": "2", "y": "2", "expected": "0"},
            "float_distance": {"x": "2", "y": "4.5", "expected": "2.5"},
    }
    invalid_test_cases = {}

class TestOperationFactory:
    """Defines the test suite for the OperationFactory class"""

    def test_valid_create(self):
        """Tests valid calls to create_operation"""
        operation_map = {
                'Addition': ops.Addition,
                'add': ops.Addition,
                '+': ops.Addition,
                'Subtraction': ops.Subtraction,
                'subtract': ops.Subtraction,
                '-': ops.Subtraction,
                'Multiplication': ops.Multiplication,
                'multiply': ops.Multiplication,
                '*': ops.Multiplication,
                'Division': ops.Division,
                'divide': ops.Division,
                '/': ops.Division,
                'Power': ops.Power,
                '^': ops.Power,
                'Root': ops.Root,
                'Modulus': ops.Modulus,
                'mod': ops.Modulus,
                'modulo': ops.Modulus,
                '%': ops.Modulus,
                'IntegerDivision': ops.IntegerDivision,
                'int_divide': ops.IntegerDivision,
                '//': ops.IntegerDivision,
                'Percentage': ops.Percentage,
                'Distance': ops.Distance,
                'abs_diff': ops.Distance
        }
        
        for op_name, op_class in operation_map.items():
            operation = ops.OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)

    def test_invalid_create(self):
        """Test invalid calls to create_operation"""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            ops.OperationFactory.create_operation("invalid_op")

    def test_valid_register(self):
        """Test valid registration parameters"""
        class TestOperation(ops.Operation):
            def execute(self, x: Decimal, y: Decimal) -> Decimal:
                return x

        ops.OperationFactory.register(TestOperation)
        operation = ops.OperationFactory.create_operation(TestOperation.__name__)
        assert isinstance(operation, TestOperation)

    def test_invalid_register(self):
        """Test invalid registration parameters"""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Registered class must inherit from Operation"):
            ops.OperationFactory.register(InvalidOperation)


