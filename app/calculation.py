"""
This module delivers a data model for storing and retrieving records of past operations

Note: The example version of this module duplicates all the arithmetic logic from Operations
in its validation, so I've pulled in the Operations module to fulfill that function.
"""
import datetime as dt
import logging as log

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, Dict

from app.calculator_config import CalculatorConfig
from app.exceptions import SerializationError, ValidationError
from app.operations import OperationFactory

@dataclass
class Calculation:
    """Record Object detailing the execution of an Operation"""
    _default_precision: ClassVar[int] = CalculatorConfig().precision

    # Dataclass will construct __init__ with these arguments
    operation: str
    operandx: Decimal
    operandy: Decimal
    result: Decimal
    
    precision: int = field(default=_default_precision)
    timestamp: dt.datetime = field(default_factory=dt.datetime.now)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Deserializes a Calculation from dictionary form.

        Includes field verification and validation.

        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary containing parameters for a single Calculation

        Raises
        ------
        SerializationError
            If data fields are missing or contain invalid values

        Returns
        -------
        Calculatio"operation": "subtract", "operandx": 5, "operandy": 3, "result": 2n
            A Calculation instance based on the input record
        """
        try:
            calc = Calculation(
                operation = data['operation'],
                operandx = Decimal(data['operandx']),
                operandy = Decimal(data['operandy']),
                result = Decimal(data['result']),
                precision = data['precision'],
            )

            calc.timestamp = dt.datetime.fromisoformat(data['timestamp'])
            calc.validate_fields()
            return calc
        except InvalidOperation:
            raise SerializationError("Error in field deserialization: Invalid data passed to Decimal()")
        except (AttributeError, KeyError) as e:
            raise SerializationError(f"Error in field deserialization: {str(e)}")

    def validate_fields(self) -> None:
        """
        Validates the operand and result fields against an Operation instance

        Logs inconsistencies in the result field without raising an Error

        Raises
        ------
        SerializationError
            If this Calculation's fields produce an invalid Operation
        """
        try:
            mock_op = OperationFactory.create_operation(self.operation)
            mock_result = mock_op.execute(self.operandx, self.operandy)\
                .quantize(Decimal('0.' + '0' * int(self.precision))).normalize()
        except ValueError:
            raise SerializationError("Data record contains an invalid operation tag")
        except ValidationError as e:
            raise SerializationError(f"Data record contains invalid operands: {str(e)}")
        if mock_result != self.result:
            log.warning(
                    f"Loaded calculation result {self.result} "
                    f"differs from computed result {mock_result}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """
        Produces a dictionary serialization of this Calculation

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of this Calculation
        """
        return {
                'operation': self.operation,
                'operandx': self.operandx,
                'operandy': self.operandy,
                'result': self.result,
                'precision': self.precision,
                'timestamp': self.timestamp.isoformat()
        }

    def __str__(self) -> str:
        """
        Generate a human-readable string detailing Calculation fields.

        Returns
        -------
        str
            a human-readable string representation of this Calculation
        """
        return f"{self.operation}({self.operandx}, {self.operandy}) = {self.result}"

    def __repr__(self) -> str:
        """
        Generate a rich string representation of this Calculation.

        Returns
        -------
        str
            A list of this Calculation's fields and their values
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operandx = {self.operandx}, "
            f"operandy = {self.operandy}, "
            f"result = {self.result}, "
            f"precision = {self.precision}, "
            f"timestamp = '{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Determines if this and another Calculation represent the same Operation

        Parameters
        ----------
        other: object
            An object to compare against this Calculation

        Returns
        -------
        bool
            True if the observed object is a Calculation with matching fields. False otherwise.
        """
        if not isinstance(other, Calculation):
            return False
        return (
            self.operation == other.operation and
            self.operandx == other.operandx and
            self.operandy == other.operandy and
            self.result == other.result
        )

