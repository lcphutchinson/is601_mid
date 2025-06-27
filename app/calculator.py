"""This module organizes and delivers the project's major features to an implementing interface"""

import logging as log
import os
import pandas as pd

from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

# Aliases
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:
    """Central business layer class for delivering features"""
    def __init__(self) -> None:
        """
        Initializes and configures the calculator

        Parameters
        ----------
        config: Optional[CalculatorConfig], optional
            Configuration settings for the application. Loaded from .env if not paased
        """

        self.config = CalculatorConfig()
        self.config.validate()
        
        os.makedirs(self.config.log_dir, exist_ok=True)
        self._setup_logging()

        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        self.observers: List[HistoryObserver] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []
        self.total: Decimal = Decimal(0)

        self._setup_directories()

        try:
            self.load_history()
        except Exception as e: # pragma: no cover
            log.warning(f"History Load failed: {e}")

        log.info("Calculator configured successfully")

    def _setup_logging(self) -> None:
        """Creates a file association for the locker"""
        try:
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            log.basicConfig(
                filename=str(log_file),
                level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True
            )
            log.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            print(f"Error setting up logging: {e}")

    def _setup_directories(self) -> None:
        """Creates directories for history management"""
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Register a new observer on the Calculator.

        Parameters
        ----------
        observer: HistoryObserver
            The Observer to register
        """
        self.observers.append(observer)
        log.info(f"Added Observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Removes and deactivates an Observer.

        Parameters
        ----------
        observer: HistoryObserver
            The Observer to reactivate
        """
        self.observers.remove(observer)
        log.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calc: Calculation) -> None:
        """
        Notifies active observers of a new Calculation object

        Parameters
        ----------
        calc: Calculation
            A newly performed Calculation
        """
        [observer.update(calc) for observer in self.observers]

    def set_operation(self, operation: Operation) -> None:
        """
        Sets the current strategy for Operation calls

        Parameters
        ----------
        operation: Operation
            The new Operation strategy to establish
        """
        self.operation_strategy = operation
        log.info(f"Set operation: {operation}")

    def perform_operation(
            self,
            x: Union[str, Number],
            y: Union[str, Number]
    ) -> CalculationResult:
        """
        Performs a Calculation using the current Operation strategy.

        Wraps input validation and history management

        Parameters
        ----------
        x: Union[str, Number]
            Raw input for the first operand
        y: Union[str, Number]
            Raw input for the second operand

        Raises
        ------
        OperationError
            If no operation strategy is set, or if its execution strategy fails
        ValidationError
            If either operand input fails to validate
        """
        if not self.operation_strategy:
            raise OperationError("No strategy set in perform_operation()")

        try:
            # Validate
            valid_x = InputValidator.validate_number(x)
            valid_y = InputValidator.validate_number(y)

            # Execute
            result = self.operation_strategy.execute(valid_x, valid_y)

            # Record
            calc = Calculation(
                operation=str(self.operation_strategy),
                operandx=valid_x,
                operandy=valid_y,
                result=result
            )
            self.undo_stack.append(CalculatorMemento(self.history.copy()))
            self.redo_stack.clear()
            self.total = result
            self.history.append(calc)
            self.notify_observers(calc)
            
            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)

            return result
        except ValidationError as e:
            log.error(f"Validation Error: {str(e)}")
            raise
        except Exception as e: # pragma: no cover
            log.error(f"Operation Failed: {str(e)}")
            raise OperationError(f"Operation Failed: {str(e)}")

    def save_history(self) -> None:
        """
        Writes the current Calculation history to file.

        Writes to CSV at the file path established in config.history_file
        
        Raises
        ------
        OperationError
            If saving is cancelled or fails
        """
        try:
            self._setup_directories()

            history_data = []
            [history_data.append(calc.to_dict()) for calc in self.history]

            if history_data:
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                log.info(f"History saved to {self.config.history_file}")
            else:
                pd.DataFrame(columns=['operation', 'operandx',\
                        'operandy', 'result', 'precision', 'timestamp']
                    ).to_csv(self.config.history_file, index=False)
                log.info("Calculation History Empty: Headers file recorded")
        except Exception as e: # pragma: no cover
            log.error(f"CSV Save Failed: {e}")
            raise OperationError(f"CSV Save Failed: {e}")

    def load_history(self) -> None:
        """
        Loads a saved Calculation history from file.

        Reads from a CSV at the path established in config.history_file

        Raises
        ------
        OperationError
            If loading is cancelled or fails
        """
        try:
            if self.config.history_file.exists():
                df = pd.read_csv(self.config.history_file)
                if not df.empty:
                    self.history = [
                        Calculation.from_dict({
                            'operation': row['operation'],
                            'operandx': row['operandx'],
                            'operandy': row['operandy'],
                            'result': row['result'],
                            'precision': row['precision'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
                    if self.history:
                        self.total = self.history[-1].result
                    log.info(f"Loaded {len(self.history)} calculations from history")
                else:
                    log.info(f"No history loaded: file empty")
            else:
                log.info(f"No history file found")
        except Exception as e:
            log.error(f"CSV Load Failed: {e}")
            raise OperationError(f"CSV Load Failed: {e}")

    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Generates a pandas DataFrame based on the current history state

        Returns
        -------
        pd.DataFrame
            A DataFrame based on the current history state
        """
        history_data = [calc.to_dict() for calc in self.history]
        return pd.DataFrame(history_data)

    def show_history(self) -> List[str]:
        """
        Produces a formatted calculation history for user viewing

        Returns
        -------
        List[str]
            A list of Calculation records in string format
        """
        return [str(calc) for calc in self.history]

    def clear_history(self) -> None:
        """Clears the calculation history and memento stacks"""
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.total = Decimal('0')
        log.info("History Cleared")

    def undo(self) -> bool:
        """
       Undoes one Operation

        Returns
        -------
        bool
            True if undo was successful. False if prior state was unavailable
        """
        if not self.undo_stack:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        if self.history:
            self.total = self.history[-1].result # pragma: no cover
        return True

    def redo(self) -> bool:
        """
        Redo a previously undone Operation

        Returns
        -------
        bool
            True if redo was successful. False if undone state was unavailable
        """
        if not self.redo_stack:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.history = memento.history.copy()
        if self.history:
            self.total = self.history[-1].result
        return True



