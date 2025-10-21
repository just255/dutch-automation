"""
Configuration Settings

This module contains configuration settings for the test framework.

Author: Claude AI
Date: 2025-10-19
"""

import os


class Config:
    """Configuration class for test framework settings."""

    # Base configuration
    BASE_URL = "https://dutch.com"

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")  # chrome, firefox, edge
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

    # Timeouts (in seconds)
    EXPLICIT_WAIT = 15           # Standard wait for interactions (click, type, select)
    PAGE_LOAD_TIMEOUT = 30       # Long operations (page loads, network calls)

    # Paths
    SCREENSHOT_PATH = "screenshots"
    REPORT_PATH = "reports"
    TEST_DATA_PATH = "config/test_data.json"

    # Screenshot settings
    ENABLE_SCREENSHOTS = os.getenv("ENABLE_SCREENSHOTS", "true").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Test execution
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "1"))
