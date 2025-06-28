"""This module provides a class structure for composing and passing commands to the calculator"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from app.calculator import Calculator
from app.exceptions import InputError, OperationError, ValidationError
from app.operations import OperationFactory

class Command(ABC):
    """Abstract base class for the Command family of classes"""
    _command_menu: str = f"\nInterface Commands\n------------------\n"

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
    
    @classmethod
    def help_menu_member(cls, com_cls: type) -> type:
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
        if not issubclass(com_cls, Command):
            raise TypeError("Registered class must inherit from Command")
        cls._command_menu += (
            f"{com_cls.__name__}: "
            f"{com_cls.execute.__doc__.strip().partition('\n')[0]}\n"
        )
        return com_cls

class ArithmeticCommand(Command):
    """Command class for launching arithmetic operations"""
    def __init__(self, ui: Any, calc: Calculator) -> None:
        """
        Registers potential command receivers

        Parameters
        ----------
        ui: Calculator_REPL
            The calling REPL instance
        calc: Calculator
            The calculator system in use this session
        """
        if not hasattr(ui, 'get_operands') or not callable(getattr(ui, 'get_operands')):
            raise TypeError("Invalid UI reference configuration")
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
        try:
            match args:
                case (command,):
                    self._op = OperationFactory.create_operation(command)
                    (x, y) = self._ui.get_operands(command)
                    self._x, self._y = x, y
                case (operand, y):
                    self._op = OperationFactory.create_operation(operand)
                    self._x, self._y = self._calc.total, y
                case (x, operand, y):
                    self._op = OperationFactory.create_operation(operand)
                    self._x, self._y = x, y
                case _: # pragma: no cover
                    return f"Invalid input format: {args}" 
            self._calc.set_operation(self._op)
            result = self._calc.perform_operation(self._x, self._y)
            return f"Result: {result}"
        except (InputError, OperationError, ValidationError, ValueError) as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

@Command.help_menu_member
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
    
    def execute(self) -> str:
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

@Command.help_menu_member
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

@Command.help_menu_member
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
        return self._command_menu + OperationFactory.op_menu

@Command.help_menu_member
class History(Command):
    """Command class for the history command"""
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
        Displays the current calculator history

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        history = self._calc.show_history()
        if not history:
            return "No history to display"
        msg = "Calculation History\n-------------------\n"
        for i, entry in enumerate(history, 1):
            msg += f"{i}. {entry}\n"
        return msg

@Command.help_menu_member
class Load(Command):
    """Command class for the load command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            the Calculator in use for this session
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Loads a saved calculation history from file

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        try:
            self._calc.load_history()
            if not self._calc.history:
                return "Load Successful, but History file was empty"
            return "Load Successful"
        except Exception as e:
            return f"Warning: History load error: {str(e)}"

@Command.help_menu_member
class Redo(Command):
    """Command class for the redo command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            the Calculator in use for this session
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Redoes the last undone calculation

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        if self._calc.redo():
            return "Redo successful"
        return "Nothing to redo"

@Command.help_menu_member
class Save(Command):
    """Command class for the save command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            the Calculator in use for this session
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Saves your calculation history to file

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        try:
            self._calc.save_history()
            return "Save Successful"
        except Exception as e:
            return f"Warning: History save failed: {str(e)}"

@Command.help_menu_member
class Undo(Command):
    """Command class for the undo command"""
    def __init__(self, calc: Calculator) -> None:
        """
        Links the command receiver

        Parameters
        ----------
        calc: Calculator
            the Calculator in use for this session
        """
        self._calc = calc

    def execute(self) -> str:
        """
        Undoes the most recent calculation

        Returns
        -------
        str
            An output message to be displayed to the user
        """
        if self._calc.undo():
            return "Undo successful"
        return "Nothing to undo"
    
