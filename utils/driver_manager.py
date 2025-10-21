"""
DriverManager Module

This module handles WebDriver initialization and configuration for multiple browsers.

Author: Claude AI
Date: 2025-10-19
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Optional
import logging


class DriverManager:
    """
    WebDriver Manager for multi-browser support.

    Supports Chrome, Firefox, and Edge browsers with automatic driver management.
    """

    def __init__(self, browser: str = "chrome", headless: bool = False):
        """
        Initialize DriverManager.

        Args:
            browser: Browser type ('chrome', 'firefox', 'edge')
            headless: Run browser in headless mode
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver: Optional[webdriver.Remote] = None
        self.logger = logging.getLogger(__name__)

    def get_chrome_driver(self) -> webdriver.Chrome:
        """
        Get Chrome WebDriver instance.

        Returns:
            Configured Chrome WebDriver
        """
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    def get_firefox_driver(self) -> webdriver.Firefox:
        """
        Get Firefox WebDriver instance.

        Returns:
            Configured Firefox WebDriver
        """
        options = webdriver.FirefoxOptions()

        if self.headless:
            options.add_argument("--headless")

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver

    def get_edge_driver(self) -> webdriver.Edge:
        """
        Get Edge WebDriver instance.

        Returns:
            Configured Edge WebDriver
        """
        options = webdriver.EdgeOptions()

        if self.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        driver.implicitly_wait(10)
        return driver

    def get_driver(self) -> webdriver.Remote:
        """
        Get WebDriver based on browser configuration.

        Returns:
            Configured WebDriver instance

        Raises:
            ValueError: If unsupported browser specified
        """
        self.logger.info(f"Initializing {self.browser} driver (headless={self.headless})")

        if self.browser == "chrome":
            self.driver = self.get_chrome_driver()
        elif self.browser == "firefox":
            self.driver = self.get_firefox_driver()
        elif self.browser == "edge":
            self.driver = self.get_edge_driver()
        else:
            raise ValueError(
                f"Unsupported browser: {self.browser}. "
                f"Supported browsers: chrome, firefox, edge"
            )

        self.logger.info(f"{self.browser.capitalize()} driver initialized successfully")
        return self.driver

    def quit_driver(self) -> None:
        """Quit the WebDriver instance."""
        if self.driver:
            self.logger.info("Quitting WebDriver")
            self.driver.quit()
            self.driver = None
