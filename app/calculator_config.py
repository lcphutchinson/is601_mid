"""This module provides an interface for accessing environment variables for global configuration"""
import os

from dataclasses import dataclass
from decimal import Decimal
from dotenv import load_dotenv
from numbers import Number
from pathlib import Path
from typing import ClassVar, Optional

from app.exceptions import ConfigurationError

@dataclass
class CalculatorConfig:
    """Container class for system configurations

    Implements the Singleton Pattern
    """
    _instance: 'CalculatorConfig' = None
    _is_configured: bool = False

    @classmethod
    def __new__(cls, *args, **kwargs) -> 'CalculatorConfig':
        """
        Class-level Singleton instantiation

        Populates the _instance field with a new CalculatorConfig, then returns
        that instance for all future calls.

        Returns
        -------
        CalculatorConfig
            The Singleton CalculatorConfig instance for this session
        """
        if not cls._instance:
            cls._instance = super(CalculatorConfig, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    ) -> None:
        """
        Initializes configuration variables from .env
        
        Parameters
        ----------
        base_dir: Path
            Base directory used during operation. Defaults to the project root
        max_history_size: int
            Value for the maximum number of stored history entries during operation.
        auto_save: bool
            Enables the auto save feature.
        precision: Optional[int], optional
            Value for the decimal precision to be used during calculations.
        max_input_value: Number
            Value for maximum numerical input.
        default_encoding: str
            Default encoding for file/IO Operations.
        """
        if self._is_configured:
            return

        load_dotenv()
        project_root = Path(__file__).parent.parent
        self.base_dir = base_dir or Path(os.getenv(
            'CALCULATOR_BASE_DIR', str(project_root)
            )).resolve()
        
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000'))

        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else \
            (auto_save_env == '1' or auto_save_env == 'true')

        self.precision = precision or \
            int(os.getenv('CALCULATOR_PRECISION', '10'))

        self.max_input_value = max_input_value or \
            Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999'))

        self.default_encoding = default_encoding or \
            os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8').lower()

        self._is_configured = True
        
    @property
    def log_dir(self) -> Path:
        """
        Get the directory path for logging files

        Returns
        -------
        Path
            The log directory path.
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR', str(self.base_dir / "logs"))).resolve()

    @property
    def history_dir(self) -> Path:
        """
        Get the directory path for history files

        Returns
        -------
        Path
            The history directory path
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """
        Get history CSV file path

        Returns
        -------
        Path
            The history file path
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()

    @property
    def log_file(self) -> Path:
        """
        Get logging file path

        Returns
        -------
        Path
            The log file path
        """
        return Path(os.getenv(
            'CALCULATOR_LOG_FILE', 
            str(self.log_dir / "calculator.log")
        )).resolve()

    def validate(self) -> None:
        """
        Validates configuration settings

        Raises
        ------
        ConfigurationError
            If the configuration contains any invalid parameters
        """
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size setting must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision setting must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value setting must be positive")


