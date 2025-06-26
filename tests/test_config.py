"""This module provides the test suites for the CalculatorConfig class and its methods"""
import pytest
import os

from decimal import Decimal
from pathlib import Path

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '500'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_PRECISION'] = '8'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_log/test_log.log'

def test_singleton_configuration():
    """Tests the singleton pattern against overwrite"""
    config = CalculatorConfig()
    config_dup = CalculatorConfig()
    assert config_dup is config

def test_sample_configurations():
    """Tests the proper assignment and accessibility of a full set of sample configurations"""
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal(1000)
    assert config.default_encoding == 'utf-16'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()
    assert config.log_file == Path('./test_log/test_log.log').resolve()

def test_fallback_configurations():
    """Tests the proper initialization of configurations in the absence of environment variables"""
    [os.environ.pop(key) for key in dict(os.environ).keys() if key.startswith("CALCULATOR")]
    config = CalculatorConfig()
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal('1e999')
    assert config.default_encoding == 'utf-8'

def test_alternate_paths():
    os.environ['CALCULATOR_BASE_DIR'] = './test_base'
    os.environ['CALCULATOR_LOG_DIR'] = './test_base/alt_log'
    os.environ['CALCULATOR_LOG_FILE'] = './test_base/alt_log/alt_log.log'
    os.environ['CALCULATOR_HISTORY_DIR'] = './test_base/alt_history'
    os.environ['CALCULATOR_HISTORY_FILE'] = './test_base/alt_history/alt_history.csv'
    config = CalculatorConfig()
    assert config.log_file == Path('./test_base/alt_log/alt_log.log').resolve()
    assert config.history_file == Path('./test_base/alt_history/alt_history.csv').resolve()

@pytest.mark.parametrize(
        "val, expected",
        [
            ('true', True),
            ('1', True),
            ('false', False),
            ('0', False)
        ],
        ids=[
            'str_truey',
            'int_truey',
            'str_falsey',
            'int_falsey'
])
def test_auto_save_vals(val: str, expected: bool):
    """Tests various formats for boolean inputs on the auto-save feature"""
    os.environ['CALCULATOR_AUTO_SAVE'] = val
    config = CalculatorConfig()
    assert config.auto_save is expected,\
        f"Expected value {expected} from input {val}"

@pytest.mark.parametrize(
        "var, expected",
        [
            ('CALCULATOR_MAX_HISTORY_SIZE', "max_history_size setting must be positive"),
            ('CALCULATOR_PRECISION', "precision setting must be positive"),
            ('CALCULATOR_MAX_INPUT_VALUE', "max_input_value setting must be positive")
        ],
        ids=[
            "negative_max_history_size",
            "negative_precision",
            "negative_max_input_size",
])
def test_invalid_parameters(var: str, expected: str):
    """Tests error handling in cases of invalid configurations"""
    [os.environ.pop(key) for key in dict(os.environ).keys() if key.startswith("CALCULATOR")]
    os.environ[var] = '-1'
    with pytest.raises(ConfigurationError, match=expected):
        config = CalculatorConfig()
        config.validate()
