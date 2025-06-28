"""This module provides the REPL interface that retrieves and directs inputs from the user"""
import logging as log

from decimal import Decimal

import app.command as cmd
from app.calculator import Calculator
from app.exceptions import InputError, OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

class Calculator_REPL():
    """Facade class that facilitates user IO"""

    def __init__(self) -> None:
        """Configures the underlying components and initializes commands"""
        self._calc = Calculator()
        self._calc.add_observer(LoggingObserver())
        self._calc.add_observer(AutoSaveObserver(self._calc))
        self._commands : dict[str, cmd.Command] = {
            'clear': cmd.Clear(self._calc),
            'exit': cmd.Exit(self._calc),
            'help': cmd.Help(self._calc),
            'history': cmd.History(self._calc),
            'load': cmd.Load(self._calc),
            'redo': cmd.Redo(self._calc),
            'save': cmd.Save(self._calc),
            'undo': cmd.Undo(self._calc)
        }
        self._arith_command = cmd.ArithmeticCommand(self, self._calc)
    
    def run(self) -> None:
        """Launches and maintains the REPL interface"""
        print("Welcome to Python REPL Calculator, v.1.6")
        print("Type 'help' for usage information, or 'exit' to quit")
        while True:
            try:
                user_input = input(f">>[{self._calc.total}]$: ").lower().strip().split()
            except EOFError:
                print("EOF Signal detected. Exiting...")
                break
            if not user_input:
                continue
            command = self._commands.get(user_input[0], self._arith_command)
            try:
                resp = command.execute() if command is not self._arith_command \
                    else command.execute(*tuple(user_input))
                print(resp)
                log.info(f"Delivered Output: {resp}")
            except Exception as e:
                print(f"Fatal Error detected: {str(e)}")
                log.error(f"Fatal Error detected: {str(e)}")
            if command == self._commands['exit']:
                break

    def get_operands(self, command: str) -> (int, int):
        """
        Requests operand inputs from the user for use in an Arithmetic command

        Parameters
        ----------
        str
            The Arithmetic Operation being called

        Raises
        ------
        InputError
            If operand inputs are cancelled

        Returns
        -------
        tuple[int, int]
            The two operand inputs entered by the user
        """
        try:
            print(f"Enter operands for command '{command}' or 'cancel' to abort:")
            x = input(">> operandx: ").lower().strip()
            if x == 'cancel':
                print(f"{command} cancelled")
                raise InputError("Command cancelled")
            y = input(">> operandy: ").lower().strip()
            if y == 'cancel':
                print(f"{command} cancelled")
                raise InputError("Command cancelled")
            return (x, y)
        except InputError:
            raise 
        except KeyboardInterrupt:
            raise InputError("Keyboard Interrupt (Ctrl+C) detected. Command cancelled")
        except Exception as e:
            raise InputError("An Unexpected Error occurred. Command cancelled")


