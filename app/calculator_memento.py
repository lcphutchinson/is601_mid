"""This module implements the Memento pattern to provide a simple undo/redo feature"""
import datetime as dt

from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.calculation import Calculation

@dataclass
class CalculatorMemento:
    """Record object detailing the Calculator history state."""

    history: List[Calculation]
    timestamp: dt.datetime = field(default_factory=dt.datetime.now)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        """
        Builds a memento from a dictionary format.

        Parameters
        ----------
        data: Dict[str, Any]
            Dictionary containing saved calculation history

        Returns
        -------
        CalculatorMemento
            A new CalculatorMemento instance with deserialized state
        """
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=dt.datetime.fromisoformat(data['timestamp'])
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the current memento state in a dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the current memento state
        """
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
