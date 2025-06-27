"""This module implements the Observer pattern to manage logging and saving"""
import logging as log

from abc import ABC, abstractmethod
from typing import Any

from app.calculation import Calculation

class HistoryObserver(ABC):
    """
    Abstract base class for the HistoryObserver family of classes.
    
    Provides an update method for implementing the Observer pattern.
    """
    @abstractmethod
    def update(self, calc: Calculation) -> None:
        """
        Handle new calculation

        Parameters
        ----------
        calc: Calculation
            The Calculation passed for logging/saving
        """
        pass # pragma: no cover

class LoggingObserver(HistoryObserver):
    """Concrete observer responsible for Calculation logging."""
    def update(self, calc: Calculation) -> None:
        """
        Adds a calculation to the log.

        Parameters
        ----------
        calc: Calculation
            The Calculation passed for logging

        Raises
        ------
        AttributeError
            if the Observer is called without a Calculation argument
        """
        if not calc:
            raise AttributeError("Error: NoneType passed to LoggingObserver")
        log.info(
            f"Calculation executed: {calc.operation} "
            f"({calc.operandx}, {calc.operandy}) = "
            f"{calc.result}"
        )

class AutoSaveObserver(HistoryObserver):
    """Concrete observer implementing the autosave function""" 
    def __init__(self, calc: Any):
        """
        Configures the AutoSaveObserver

        Parameters
        ----------
        calc: Any
            A link to the implementing Calculator instance
                Must have the 'config' and 'save_history' attributes

        Raises
        ------
        TypeError
            if the implementing Calculator isn't properly configured
        """
        if not hasattr(calc, 'config') or not hasattr(calc, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calc

    def update(self, calc: Calculation) -> None:
        """
        Execute an auto-save.

        Parameters
        ----------
        calc: Calculation
            The Calculation passed for saving

        Raises
        ------
        AttributeError
            if the Observer is called without a Calculation argument
        """
        if not calc:
            raise AttributeError("Error: NoneType passed to AutoSaveObserver")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            log.info("Auto-save Completed")


