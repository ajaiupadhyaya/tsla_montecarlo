"""
Quantitative Finance Framework - A comprehensive toolkit for quantitative research and trading.
"""

__version__ = "0.1.0"

from .config import Config
from .utils.logging import setup_logging
from .data_prep import DataLoader
from .alpha_models import AlphaModel
from .backtesting import BacktestEngine
from .nlp import NLPProcessor

# Initialize logging
setup_logging()

__all__ = [
    "Config",
    "DataLoader",
    "AlphaModel",
    "BacktestEngine",
    "NLPProcessor",
] 