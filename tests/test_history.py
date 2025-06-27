"""This module provides the test suites for the HistoryObserver family of classes"""
import pytest

from unittest.mock import Mock, patch

from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

CalculatorConfig._is_configured = False

calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.operandx = 8
calculation_mock.operandy = 6
calculation_mock.result = 14

calculator_mock = Mock(spec=Calculator)
calculator_mock.config = Mock(spec=CalculatorConfig)
calculator_mock.config.auto_save = True
calculator_mock.config.precision = 10

@patch('logging.info')
def test_logging_observer_log(logging_info_mock):
    """Tests that the LoggingObserver logs a valid Calculation"""
    observer = LoggingObserver()
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        "Calculation executed: addition (8, 6) = 14"
    )

def test_logging_observer_empty_log():
    """Tests LoggingObserver error handling"""
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)

def test_autosave_observer_call():
    """Tests a call to AutoSaveObserver"""
    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()

@patch('logging.info')
def test_autosave_observer_save(logging_info_mock):
    """Tests that the AutoSaveObserver successfully saves"""
    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        "Auto-save Completed"
    )

def test_autosave_observer_off():
    """Tests conditions of AutoSaveObserver's save behavior"""
    calculator_mock.reset_mock()
    calculator_mock.config.auto_save = False
    observer = AutoSaveObserver(calculator_mock)
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_not_called()

def test_autosave_observer_empty_save():
    """Tests AutoSaveObserver's error handling of an empty save call"""
    observer = AutoSaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None)

def test_autosave_observer_no_config():
    """Tests AutoSaveObserver's error handling of an invalid config"""
    with pytest.raises(TypeError):
        AutoSaveObserver(None)

