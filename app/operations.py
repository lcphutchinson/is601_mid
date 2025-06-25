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

class OperationFactory:
    """Factory class for the Operation class family"""

    _operations: Dict[str, type] = {}

    @classmethod
    def register(cls, op_cls: type) -> None:
        """
        Decorator for Operation subclass registration

        Adds an Operation class to the _operations dict under its class name,
        as well as any names in the classes _aliases list, if it has one.

        Parameters
        ----------
        op_cls: type
            The Operation class to register

        Raises
        ------
        TypeError
            If a class outside the Operation family is registered
        """
        if not issubclass(op_cls, Operation):
            raise TypeError("Registered class must inherit from Operation")
        cls._operations[op_cls.__name__.lower()] = op_cls
        if hasattr(op_cls, "_aliases"):
            for alias in op_cls._aliases:
                cls._operations[alias] = op_cls
        return op_cls

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

@OperationFactory.register
class Addition(Operation):
    """Concrete Product for addition operations"""
    _aliases = ['add', '+']

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

@OperationFactory.register
class Subtraction(Operation):
    """Concrete Product for subtraction operations"""
    _aliases = ['subtract', '-']

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

@OperationFactory.register
class Multiplication(Operation):
    """Concrete Product for multiplication operations"""
    _aliases = ['multiply', '*']
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

@OperationFactory.register
class Division(Operation):
    """Concrete Product for division operations"""
    _aliases = ['divide', '/']

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

@OperationFactory.register
class Power(Operation):
    """Concrete Product for exponent operations"""
    _aliases = ['^']

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

@OperationFactory.register
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

@OperationFactory.register
class Modulus(Operation):
    """Concrete Product for modulo operations"""
    _aliases = ['mod', 'modulo', '%']

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs a modulo division using two operands

        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand
        
        Returns
        -------
        Decimal
            The remainder produced by a division of x by y
        """
        return x % y

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Prechecks for a zero divisor

        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand

        Raises
        ------
        ValidationError
            If a zero divisor is detected
        """
        if y == 0:
            raise ValidationError("Divisor operand cannot be 0")

@OperationFactory.register
class IntegerDivision(Operation):
    """Concrete Product for integer division operations"""
    _aliases = ['int_divide', '//']

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Performs an integer division using two operands

        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand

        Returns
        -------
        Decimal
            The quotient value x / y, rounded down to an integer value
        """
        return (x / y).quantize('1.0', rounding=ROUND_FLOOR)

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Prechecks for a zero divisor

        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand

        Raises
        ------
        ValidationError
            If a zero divisor is detected
        """
        if y == 0:
            raise ValidationError("Divisor operand cannot be 0")
        
@OperationFactory.register
class Percentage(Operation):
    """Concrete Product for percentage operations"""

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Constructs a percentage using two operands
        
        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand

        Returns
        -------
        Decimal
            The ratio of x to y, expressed as a percentage
        """
        return x / y * 100

    def validate_operands(self, x: Decimal, y: Decimal) -> None:
        """
        Prechecks for a zero divisor

        Parameters
        ----------
        x: Decimal
            Dividend operand
        y: Decimal
            Divisor operand

        Raises
        ------
        ValidationError
            If a zero divisor is detected
        """
        if y == 0:
            raise ValidationError("Divisor operand cannot be 0")

@OperationFactory.register
class Distance(Operation):
    """Concrete Product for distance operations"""
    _aliases = ['abs_diff']

    def execute(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Calculates the distance between two operands

        Parameters
        ----------
        x: Decimal
            Minuend operand
        y: Decimal
            Subtrahend operand

        Returns
        -------
        Decimal
            The absolute difference, or distance, between x and y
        """
        return abs(x - y)


















































































