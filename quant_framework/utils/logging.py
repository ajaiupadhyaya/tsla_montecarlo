"""
Logging configuration for the quantitative finance framework.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from ..config import Config

def setup_logging(log_file: Optional[str] = None):
    """
    Set up logging configuration for the framework.
    
    Args:
        log_file: Optional path to log file. If None, uses config value.
    """
    config = Config()
    
    # Get logging configuration
    log_config = config.get("logging", {})
    log_level = getattr(logging, log_config.get("level", "INFO"))
    log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Create logs directory if it doesn't exist
    if log_file is None:
        log_file = log_config.get("file", "logs/quant_framework.log")
    
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Add file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config.get("max_size", 10 * 1024 * 1024),  # 10MB default
        backupCount=log_config.get("backup_count", 5)
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set logging levels for specific modules
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("tensorflow").setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module/logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name) 