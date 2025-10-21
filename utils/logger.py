"""
Logger Module

This module provides logging configuration with colorlog support.

Author: Claude AI
Date: 2025-10-19
"""

import logging
import colorlog
import os
from datetime import datetime


def setup_logger(name: str = __name__, log_level: str = "INFO") -> logging.Logger:
    """
    Setup and configure logger with color support.

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Console handler with color support
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Color formatter
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
