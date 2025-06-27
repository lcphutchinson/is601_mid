"""This module provides the test suite for IO operations in calculator_repl"""
import pytest

from unittest.mock import Mock, patch

from app.calculator_repl import calculator_repl

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Thank you for using Python REPL Calculator. Exiting...")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Available Commands")

@patch('builtins.input', side_effect=['add', '6', '8', 'history', \
        'save', 'load', 'undo', 'redo', 'clear', 'history', 'exit'])
@patch('builtins.print')
def test_calculator_repl_history(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Calculation History")
    mock_print.assert_any_call("1. Addition(6, 8) = 14")
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
    calculator_repl()
    mock_print.assert_any_call("multiply cancelled")
    mock_print.assert_any_call("subtract cancelled")
    mock_print.assert_any_call("Error: Divisor operand cannot be 0")
    mock_print.assert_any_call("Unknown command: 'nonsense'. Type 'help' for available commands.")
    mock_print.reset_mock()
    mock_input.reset_mock()
