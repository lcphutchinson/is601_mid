"""This module provides a class structure for composing and passing commands to the calculator"""
from abc import ABC, abstractmethod
from decimal import Decimal

from app/calculator import Calculator
from app/calculator_repl import Calculator_REPL
from app/exceptions import InputError
from app/operations import OperationFactory

command_menu: str = f"Interface Commands\n------------------\n"

class Command(ABC):
    """Abstract base class for the Command family of classes"""
    
    @abstractmethod
    def execute(self) -> str:
        """
        Performs the underlying action associated with the Command

        Must be implemented by child classes
        
        Returns
        -------
        str
            Output text associated with the command or any error raised
        """
        pass # pragma: no cover

def help_menu_member(com_cls: type) -> type:
    """
    Command decorator for constructing output for the 'help' command

    Parameters
    ----------
    com_cls: type
        A subclass of Command for parsing

    Raises
    ------
    TypeError
        If a class outside the Command family is passed
    """
    if not issubclass(op_cls, Command):
        raise TypeError("Registered class must inherit from Command")
    command_menu += (
            f"{op_cls.__name__}: "
            f"{op_cls.execute.__doc__.strip().partition('\n')[0]}\n"
    )
    return op_cls

class ArithmeticCommand(Command):
    """Command class for launching arithmetic operations"""
    def __init__(self, ui: Calculator_REPL, calc: Calculator) -> None:
        """
        Registers potential command receivers

        Parameters
        ----------
        ui: Calculator_REPL
            The calling REPL instance
        calc: Calculator
            The calculator system in use this session
        """
        self._ui = ui
        self._calc = calc

    def execute(self, *args) -> str:
        """
        Organizes the operation parameters and passes them on to the Calculator

        Parameters
        ----------
        args: tuple
            The Operation type and its operands

        Returns
        -------
        str
            An output message to be displayed to the user.
        """
        # Parse multiple input formats
        match args:
            case (command):
                try:
                    (x, y) = self._ui.get_operands()
                    self._command, self._x, self._y = command, x, y
                except InputError as e:
                    return str(e)
            case (operand, y):
                self._command, self._x, self._y = operand, self._calc.total, y
            case (x, operand, y):
                self._command, self._x, self._y = operand, x, y
            case _:
                pass
        try:
            op = OperationFactory.create_operation(self._command)
            self._calc.set_operation(op)
            result = self._calc.perform_operation(self._x, self._y)
            if isinstance(result, Decimal):
                result = result.normalize()
            return f"Result: {result}"
        except (OperationError, ValidationError) as e:
            return f"Error: {str(e)}"
        except Exception as e: # pragma: no cover
            return f"Unexpected Error: {str(e)}"

@help_menu_member
class Clear(Command):
    """Command class for the clear command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            The calculator in use for this session
        """
        self._calc = calc
    
    def execute(self) -> str
        """
        Clears the current operation history

        Returns
        -------
        str
            An output message to be displayed to the user.
        """
        try:
            self._calc.clear_history()
            return "History cleared"
        except Exception as e:
            return f"Error: {str(e)}"

@help_menu_member
class Exit(Command):
    """Command class for the exit command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            The calculator in use for this session            
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Saves the current history and exits the Calculator
        
        Returns
        -------
        str
            An output message to be displayed to the user
        """
        exit_msg = "\n\nThank you for using Python REPL Calculator. Exiting..."
        try:
            self._calc.save_history()
            exit_msg = "History Saved Successfully" + exit_msg
        except Exception as e:
            exit_msg = f"Warning: History save error: {str(e)}" + exit_msg
        return exit_msg

@help_menu_member
class Help(Command):
    """Command class for the help command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameter
        ---------
        calc: Calculator
            The calculator in use for this session
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Displays a list of available commands

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        return command_menu + OperationFactory.op_menu


