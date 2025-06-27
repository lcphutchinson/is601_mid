"""This module provides a test suite for the Calculator class in app.calculator"""
import datetime
import pandas as pd
import pytest

from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch, PropertyMock
from tempfile import TemporaryDirectory

from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        with patch.object(CalculatorConfig, 'log_dir', \
            new_callable=PropertyMock) as mock_log_dir, \
            patch.object(CalculatorConfig, 'log_file', \
            new_callable=PropertyMock) as mock_log_file, \
            patch.object(CalculatorConfig, 'history_dir', \
            new_callable=PropertyMock) as mock_history_dir, \
            patch.object(CalculatorConfig, 'history_file', \
            new_callable=PropertyMock) as mock_history_file:

            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"

            yield Calculator(config=config)
        
def test_calculator_init(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

@patch('app.calculator.log.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', \
        new_callable=PropertyMock) as mock_log_dir, \
        patch.object(CalculatorConfig, 'log_file', \
        new_callable=PropertyMock) as mock_log_file:

        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator configured successfully")

def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

def test_set_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

def test_perform_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(8, 6)
    assert result == Decimal('14')

def test_overflow_history(calculator):
    calculator.config.max_history_size = 1
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    calculator.perform_operation(8, 6)
    assert len(calculator.history) == 1

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('nonsense', 6)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No strategy set in perform_operation()"):
        calculator.perform_operation(8, 6)

def test_undo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

def test_undo_unavailable(calculator):
    assert calculator.undo() == False

def test_redo_unavailable(calculator):
    assert calculator.redo() == False

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.log.info')
def test_save_collumns(logging_info_mock, calculator):
    calculator.save_history()
    logging_info_mock.assert_any_call("Calculation History Empty: Headers file recorded")


@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['add'],
        'operandx': ['8'],
        'operandy': ['6'],
        'result': ['14'],
        'precision': ['10'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })

    try:
        calculator.load_history()
        assert len(calculator.history) == 1
        assert calculator.history[0].operation == 'add'
        assert calculator.history[0].operandx == Decimal('8')
        assert calculator.history[0].operandy == Decimal('6')
        assert calculator.history[0].result == Decimal('14')
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists')
def test_load_empty(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame()

    calculator.load_history()
    assert len(calculator.history) == 0

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists')
def test_load_invalid(mock_exists, mock_read_csv, calculator):
    with pytest.raises(OperationError):
        mock_read_csv.return_value = None
        calculator.load_history()

def test_clear_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    
def test_get_dataframe(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(8, 6)
    df = calculator.get_history_dataframe()
    assert isinstance(df, pd.DataFrame)
