"""This module provides a class structure for composing and executing arithmetic operations"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict

from app.exceptions import ValidationError

class Operation(ABC):
    """
    Abstract base class for the Operation family of classes.

    Serves as an Abstract Product for OperationFactory
    """

    @abstractmethod
    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Perform's the class's underlying arithmetic on its stored operands.

        Must be implemented by child classes.

        Parameters
        ----------
        x : Decimal
            First operand
        y : Decimal
            Second operand

        Returns
        -------
        Decimal
            The result of the class's arithmetic operation.
        """
        pass # pragma: no cover

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Validate's the class's operands for execution.

        Override for operations requiring specific pre-execution checks, like Division

        Parameters
        ----------
        x : Decimal
            First operand
        y : Decimal
            Second operand
        """
        pass # pragma: no cover

    def __str__(self) -> str:
        """
        Defines the string representation of inheriting subclasses

        Returns
        -------
        str
            The name of the implementing Operation
        """
        return self.__class__.__name__

class Addition(Operation):
    """Concrete Product for addition operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Adds two Decimal operands

        Parameters
        ----------
        x : Decimal
            Augend operand
        y : Decimal
            Addend operand

        Returns
        -------
        Decimal
            The sum of x and y
        """
        return x + y

class Subtraction(Operation):
    """Concrete Product for subtraction operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs a subtraction using two operands

        Parameters
        ----------
        x : Decimal
            Minuend operand
        y : Decimal
            Subtrahend operand

        Returns
        -------
        Decimal
            The difference of y from x
        """
        return x - y

class Multiplication(Operation):
    """Concrete Product for multiplication operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Multiplies two Decimal operands

        Parameters
        ----------
        x : Decimal
            Multiplicand operand
        y : Decimal
            Multiplier operand

        Returns
        -------
        Decimal
            The product of x and y
        """
        return x * y

class Division(Operation):
    """Concrete Product for division operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs a division using two operands

        Parameters
        ----------
        x : Decimal
            Dividend operand
        y : Decimal
            Divisor operand

        Returns
        -------
        Decimal
            The quotient x / y
        """
        self.validate_operands(x, y)
        return x / y

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Prechecks operands for a zero divisor.

        Parameters
        ----------
        x : Decimal
            Dividend operand
        y : Decimal
            Divisor operand

        Raises
        ------
        ValidationError
            If a zero divisor is detected
        """
        super().validate_operands(x, y)
        if y == 0:
            raise ValidationError("Divisor operand cannot be 0")

class Power(Operation):
    """Concrete Product for exponent operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs an exponentiation using two operands

        Parameters
        ----------
        x : Decimal
            Base operand
        y : Decimal
            Exponent operand

        Returns
        -------
        Decimal
            A value representing x ^ y
        """
        if x == 0:
            return Decimal(0)
        if y < 0:
            return Decimal(1 / pow(float(x), float(y * -1)))
        return Decimal(pow(float(x), float(y)))

class Root(Operation):
    """Concrete Product for root operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs a root operation using two operands

        Parameters
        ----------
        x : Decimal
            Degree operand
        y : Decimal
            Radicand operand

        Return
        ------
        Decimal
            The yth root of x
        """
        self.validate_operands(x, y)
        if x == 0:
            return Decimal(0)
        (base, sign) = (x * -1, -1) if x < 0 else (x, 1)
        if y < 0:
            return Decimal(sign / pow(float(base), 1 / float(y * -1)))
        return Decimal(sign * pow(float(base), 1 / float(y)))

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Prechecks operands for imaginary or undefined root conditions

        Parameters
        ----------
        x : Decimal
            Degree operand
        y : Decimal
            Radicand operand

        Raises
        ------
        ValidationError
            If a zero radicand or even radicand over a negative degree is detected
        """
        super().validate_operands(x, y)
        if x < 0 and y % 2 == 0:
            raise ValidationError("Imaginary roots not supported")
        if y == 0:
            raise ValidationError("Zero radicand is undefined")

class OperationFactory:
    """Factory class for the Operation class family"""

    _operations: Dict[str, type] = {
            'add': Addition,
            'addition': Addition,
            'subtract': Subtraction,
            'subtraction': Subtraction,
            'multiply': Multiplication,
            'multiplication': Multiplication,
            'divide': Division,
            'division': Division,
            'power': Power,
            'root': Root,
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Registers an operation class to the Factory

        Parameters
        ----------
        name : str
            text identifier for the operation
        operation_class : type
            class implementation of the operation

        Raises
        ------
        TypeError
            If a class outside the Operation family is registered
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Registered class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Instantiates an Operations subclass by string identifier.

        Parameters
        ----------
        operation_type : str
            a string identifier for the desired Operation

        Raises
        ------
        ValueError
            If the provided operation_type is not registered to the Factory

        Returns
        -------
        Operation
            an instance of the specified Operation subclass
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()


