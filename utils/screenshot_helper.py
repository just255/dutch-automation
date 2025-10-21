"""
ScreenshotHelper Module

This module provides screenshot capture utilities with element highlighting.

Author: Claude AI
Date: 2025-10-19
"""

import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Optional
import logging
from PIL import Image, ImageDraw


class ScreenshotHelper:
    """Helper class for capturing screenshots during test execution with element highlighting."""

    def __init__(self, driver: webdriver.Remote, screenshots_dir: str = "screenshots"):
        """
        Initialize ScreenshotHelper.

        Args:
            driver: Selenium WebDriver instance
            screenshots_dir: Directory to save screenshots
        """
        self.driver = driver
        self.screenshots_dir = screenshots_dir
        self.logger = logging.getLogger(__name__)

        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def capture(self, name: str, subfolder: Optional[str] = None, element: Optional[WebElement] = None) -> str:
        """
        Capture screenshot with optional element highlighting.

        Args:
            name: Screenshot name (without extension)
            subfolder: Optional subfolder within screenshots_dir
            element: Optional WebElement to highlight with red box

        Returns:
            Full path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"

        # Determine save path
        if subfolder:
            save_dir = os.path.join(self.screenshots_dir, subfolder)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            filepath = os.path.join(save_dir, filename)
        else:
            filepath = os.path.join(self.screenshots_dir, filename)

        try:
            # Capture base screenshot
            self.driver.save_screenshot(filepath)

            # If element provided, add red highlight box
            if element:
                self._add_element_highlight(filepath, element)

            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return ""

    def _add_element_highlight(self, image_path: str, element: WebElement) -> None:
        """
        Add red highlight box around element in screenshot.

        Args:
            image_path: Path to screenshot image
            element: WebElement to highlight
        """
        try:
            # Get element location and size
            location = element.location
            size = element.size

            # Calculate coordinates for red box
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']

            # Open image with PIL
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # Draw red rectangle around element (5 pixel width)
            for i in range(5):
                draw.rectangle(
                    [(left - i, top - i), (right + i, bottom + i)],
                    outline='red'
                )

            # Save modified image
            img.save(image_path)
            self.logger.info(f"Added element highlight to screenshot: {image_path}")

        except Exception as e:
            self.logger.warning(f"Failed to add element highlight: {e}")

    def capture_on_failure(self, test_name: str) -> str:
        """
        Capture screenshot on test failure.

        Args:
            test_name: Name of failed test

        Returns:
            Full path to saved screenshot
        """
        # Capture screenshot
        screenshot_path = self.capture(f"FAILED_{test_name}", subfolder="failures")

        # Capture HTML source
        self.capture_html_source(test_name)

        return screenshot_path

    def capture_html_source(self, test_name: str) -> str:
        """
        Capture HTML page source on test failure.

        Args:
            test_name: Name of test

        Returns:
            Full path to saved HTML file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FAILED_{test_name}_{timestamp}.html"

        # Create failures subfolder if doesn't exist
        failures_dir = os.path.join(self.screenshots_dir, "failures")
        if not os.path.exists(failures_dir):
            os.makedirs(failures_dir)

        filepath = os.path.join(failures_dir, filename)

        try:
            # Get page source
            page_source = self.driver.page_source

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_source)

            self.logger.info(f"HTML source saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to capture HTML source: {e}")
            return ""

    def capture_element(self, element: WebElement, name: str) -> str:
        """
        Capture screenshot of specific element.

        Args:
            element: WebElement to capture
            name: Screenshot name

        Returns:
            Full path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)

        try:
            element.screenshot(filepath)
            self.logger.info(f"Element screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to capture element screenshot: {e}")
            return ""
