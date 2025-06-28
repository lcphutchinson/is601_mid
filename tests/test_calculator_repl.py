"""This module provides the test suite for IO operations in calculator_repl"""
import pytest

from unittest.mock import Mock, patch

from app.calculator_repl import Calculator_REPL

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        Calculator_REPL().run()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call(
            "History Saved Successfully\n"
            "\nThank you for using Python REPL Calculator. Exiting..."
        )

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    Calculator_REPL().run()
    mock_print.assert_any_call("""
Interface Commands
------------------
Clear: Clears the current operation history
Exit: Saves the current history and exits the Calculator
Help: Displays a list of available commands
History: Displays the current calculator history
Load: Loads a saved calculation history from file
Redo: Redoes the last undone calculation
Save: Saves your calculation history to file
Undo: Undoes the most recent calculation

Arithmetic Commands
-------------------
<command> [<alias>]: <description>
----------------------------------
Addition ['add', '+']: Adds two Decimal operands
Subtraction ['subtract', '-']: Performs a subtraction using two operands
Multiplication ['multiply', '*']: Multiplies two Decimal operands
Division ['divide', '/']: Performs a division using two operands
Power ['^']: Performs an exponentiation using two operands
Root []: Performs a root operation using two operands
Modulus ['mod', 'modulo', '%']: Performs a modulo division using two operands
IntegerDivision ['int_divide', '//']: Performs an integer division using two operands
Percentage []: Constructs a percentage using two operands
Distance ['abs_diff']: Calculates the distance between two operands
"""
    )

@patch('builtins.input', side_effect=['add', '6', '8', 'history', \
        'save', 'load', 'undo', 'redo', 'clear', 'history', 'exit'])
@patch('builtins.print')
def test_calculator_repl_history(mock_print, mock_input):
    Calculator_REPL().run()
    mock_print.assert_any_call(
            "Calculation History\n-------------------\n"
            "1. Addition(6, 8) = 14\n"
    )
    mock_print.assert_any_call("Save Successful")
    mock_print.assert_any_call("Load Successful")
    mock_print.assert_any_call("Undo successful")
    mock_print.assert_any_call("Redo successful")
    mock_print.assert_any_call("History cleared")
    mock_print.assert_any_call("No history to display")
    mock_print.reset_mock()
    mock_input.reset_mock()
    

@patch('builtins.input', side_effect=['multiply', 'cancel', 'subtract', '8', \
        'cancel', 'divide', '5', '0', 'nonsense', 'exit'])
@patch('builtins.print')
def test_calculator_repl_cancel(mock_print, mock_input):
    Calculator_REPL().run()
    mock_print.assert_any_call("multiply cancelled")
    mock_print.assert_any_call("subtract cancelled")
    mock_print.assert_any_call("Error: Divisor operand cannot be 0")
    mock_print.assert_any_call("Error: Unknown operation: 'nonsense'")
    mock_print.reset_mock()
    mock_input.reset_mock()

@patch('builtins.input', side_effect=['8 + 6', '- 4', '2 * 2', '^ 2', 'exit'])
@patch('builtins.print')
def test_calculator_repl_alternate_input_modes(mock_print, mock_input):
    Calculator_REPL().run()
    mock_print.assert_any_call("Result: 14")
    mock_print.assert_any_call("Result: 10")
    mock_print.assert_any_call("Result: 4")
    mock_print.assert_any_call("Result: 16")
