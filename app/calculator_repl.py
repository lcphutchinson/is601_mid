"""This module provides the REPL interface that retrieves and directs inputs from the user"""
import logging as log

from decimal import Decimal

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

def calculator_repl():
    """Launches and maintains the REPL interface"""
    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Welcome to Python REPL Calculator, v.1.5")
        print("Type 'help' for usage information, or 'exit' to quit")
        while True:
            try:
                command = input(">>$: ").lower().strip()
                
                match command:
                    case 'help':
                        print("Available Commands")
                        print("------------------")
                        print("add, subtract, multiply, divide, power, root -- Perform calculations")
                        print("history - Display your calculation history")
                        print("clear - Clear your calculation history")
                        print("undo - Undo your last calculation")
                        print("redo - Redo the last undone calculation")
                        print("save - Save calculation history to file")
                        print("load - Load calculation history from file")
                        print("exit - Exit the calculator")
                    
                    case 'exit':
                        try:
                            calc.save_history()
                            print("History saved successfully.")
                        except Exception as e: # pragma: no cover
                            print(f"Warning: History save failed: {e}")
                        print("Thank you for using Python REPL Calculator. Exiting...")
                        break
                    
                    case 'history':
                        history = calc.show_history()
                        if not history:
                            print("No history to display")
                        else:
                            print("Calculation History")
                            print("-------------------")
                            [print(f"{i}. {entry}") for i, entry in enumerate(history, 1)]

                    case 'clear':
                        calc.clear_history()
                        print("History cleared")

                    case 'undo':
                        print("Undo successful") if calc.undo() else print("Nothing to undo")

                    case 'redo':
                        print("Redo successful") if calc.redo() else print("Nothing to redo")

                    case 'save':
                        try:
                            calc.save_history()
                            print("Save Successful")
                        except Exception as e: # pragma: no cover
                            print(f"Warning: Save failed: {e}")

                    case 'load':
                        try:
                            calc.load_history()
                            print("Load Successful")
                        except Exception as e: # pragma: no cover
                            print(f"Warning: Load failed: {e}")

                    case 'add' | 'subtract' | 'multiply' | 'divide' | 'power' | 'root':
                        try:
                            print(f"Enter operands for command '{command}', or 'cancel' to abort:")
                            x = input(">> operandx: ").lower().strip()
                            if x == 'cancel':
                                print(f"{command} cancelled")
                                continue
                            y = input(">> operandy: ").lower().strip()
                            if y == 'cancel':
                                print(f"{command} cancelled")
                                continue

                            op = OperationFactory.create_operation(command)
                            calc.set_operation(op)

                            result = calc.perform_operation(x, y)
                            if isinstance(result, Decimal):
                                result = result.normalize()

                            print(f"Result: {result}")
                        except (OperationError, ValidationError) as e:
                            print(f"Error: {e}")
                        except Exception as e: # pragma: no cover
                            print(f"Unexpected error during operand entry: {e}")
                    
                    case _:
                        print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt: # pragma: no cover
                print("Keyboard Interrupt (Ctrl+C) detected. Input cancelled")
            except EOFError: # pragma: no cover
                print("EOF signal detected. Exiting...")
                break
            except Exception as e: # pragma: no cover
                print(f"Unexpected Error: {e}")

    except Exception as e: # pragma: no cover
        print(f"Fatal error detected: {e}")
        log.error(f"Fatal error in REPL: {e}")
        raise


