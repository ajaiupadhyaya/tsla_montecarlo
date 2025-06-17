"""
Alpha model base class for the quantitative finance framework.
"""

from typing import Any, Dict, Optional
import pandas as pd
from ..utils.logging import get_logger

logger = get_logger(__name__)

class AlphaModel:
    """
    Base class for all alpha signal generators (RL, DL, ML, NLP, Alternative).
    """
    def __init__(self, config: Optional[Any] = None):
        self.config = config
        logger.info(f"Initialized {self.__class__.__name__}")

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> None:
        """
        Fit the model to data.
        """
        raise NotImplementedError("fit() must be implemented by subclasses.")

    def predict(self, X: pd.DataFrame) -> Any:
        """
        Generate alpha signals or predictions.
        """
        raise NotImplementedError("predict() must be implemented by subclasses.")

    def save(self, path: str) -> None:
        """
        Save the model to disk.
        """
        raise NotImplementedError("save() must be implemented by subclasses.")

    def load(self, path: str) -> None:
        """
        Load the model from disk.
        """
        raise NotImplementedError("load() must be implemented by subclasses.") 