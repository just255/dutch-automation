"""
BasePage Module

This module contains the BasePage class which serves as the foundation for all page objects.
It provides generic utility methods and universal UI elements that are common across all pages.

Author: Claude AI
Date: 2025-10-19
"""

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from typing import Tuple, Optional
import time
import os


class BasePage:
    """
    BasePage class containing generic utility methods and universal UI elements.

    This class should ONLY contain:
    - Generic utility methods (click, type, wait, scroll, etc.)
    - Universal UI elements (generic loading spinners, error messages that appear site-wide)

    Component-specific elements (headers, footers, navigation) belong in separate component classes.
    """

    _screenshot_counter = 0  # Class variable for sequential numbering

    def __init__(self, driver, screenshot_helper=None, config=None):
        """
        Initialize BasePage with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            screenshot_helper: Optional screenshot helper for automatic screenshots
            config: Optional config object for timeouts and screenshot settings
        """
        self.driver = driver
        # Use config timeouts if provided, otherwise use defaults
        explicit_wait = config.EXPLICIT_WAIT if config else 15
        page_load_timeout = config.PAGE_LOAD_TIMEOUT if config else 30
        self.wait = WebDriverWait(driver, explicit_wait)
        self.long_wait = WebDriverWait(driver, page_load_timeout)
        self.screenshot_helper = screenshot_helper
        self.config = config

    def _auto_screenshot(self, action_name: str, element_name: str = "") -> None:
        """
        Automatically capture screenshot if enabled in config.

        Args:
            action_name: Name of the action (e.g., 'click', 'enter_text')
            element_name: Optional element identifier
        """
        if self.screenshot_helper and self.config and self.config.ENABLE_SCREENSHOTS:
            BasePage._screenshot_counter += 1
            # Create screenshot name: counter_action_element
            counter_str = f"{BasePage._screenshot_counter:03d}"
            element_part = f"_{element_name}" if element_name else ""
            screenshot_name = f"{counter_str}_{action_name}{element_part}"
            self.screenshot_helper.capture(screenshot_name)

    # ==================== GENERIC UTILITY METHODS ====================

    def click_element(self, locator: Tuple, timeout: int = 10) -> None:
        """
        Click an element with explicit wait and scroll into view.
        Retries with JavaScript click if regular click is intercepted.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Raises:
            TimeoutException: If element not clickable within timeout
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll element into view to avoid interception
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

            try:
                element.click()
            except ElementClickInterceptedException:
                # If click is intercepted, wait for element to be stable and retry with JS click
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(locator)
                )
                self.driver.execute_script("arguments[0].click();", element)

            # Auto-screenshot after click
            element_name = str(locator[1])[:30] if len(locator) > 1 else "element"
            self._auto_screenshot("click", element_name)
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not clickable after {timeout}s"
            )

    def enter_text(self, locator: Tuple, text: str, timeout: int = 10) -> None:
        """
        Clear and enter text into an input field.

        Args:
            locator: Tuple of (By.TYPE, "value")
            text: Text to enter
            timeout: Maximum wait time in seconds

        Raises:
            TimeoutException: If element not visible within timeout
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
            # Auto-screenshot after entering text
            element_name = str(locator[1])[:30] if len(locator) > 1 else "input"
            self._auto_screenshot("enter_text", element_name)
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not visible after {timeout}s"
            )

    def select_dropdown_by_text(self, locator: Tuple, text: str, timeout: int = 10) -> None:
        """
        Select dropdown option by visible text.

        Args:
            locator: Tuple of (By.TYPE, "value")
            text: Visible text of option to select
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        select = Select(element)
        select.select_by_visible_text(text)
        # Auto-screenshot after selection
        element_name = str(locator[1])[:30] if len(locator) > 1 else "dropdown"
        self._auto_screenshot("select_dropdown", element_name)

    def select_dropdown_by_value(self, locator: Tuple, value: str, timeout: int = 10) -> None:
        """
        Select dropdown option by value attribute.

        Args:
            locator: Tuple of (By.TYPE, "value")
            value: Value attribute of option to select
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        select = Select(element)
        select.select_by_value(value)
        # Auto-screenshot after selection
        element_name = str(locator[1])[:30] if len(locator) > 1 else "dropdown"
        self._auto_screenshot("select_dropdown", element_name)

    def wait_for_element(self, locator: Tuple, timeout: int = 10) -> bool:
        """
        Wait for element to be present in DOM.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if element found, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator: Tuple, timeout: int = 10) -> bool:
        """
        Wait for element to be visible.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if element visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_invisible(self, locator: Tuple, timeout: int = 10) -> bool:
        """
        Wait for element to become invisible.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if element invisible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator: Tuple, timeout: int = 10) -> None:
        """
        Scroll element into view.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Brief pause after scroll
        # Auto-screenshot after scroll
        element_name = str(locator[1])[:30] if len(locator) > 1 else "element"
        self._auto_screenshot("scroll_to_element", element_name)

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        # Auto-screenshot after scroll
        self._auto_screenshot("scroll_to_bottom")

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        # Auto-screenshot after scroll
        self._auto_screenshot("scroll_to_top")

    def take_screenshot(self, name: str, path: str = "screenshots") -> str:
        """
        Capture screenshot with given name.

        Args:
            name: Screenshot filename (without extension)
            path: Directory path for screenshot

        Returns:
            Full path to saved screenshot
        """
        # Ensure screenshots directory exists
        if not os.path.exists(path):
            os.makedirs(path)

        # Generate filename with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(path, filename)

        # Capture and save screenshot
        self.driver.save_screenshot(filepath)
        return filepath

    def navigate_to(self, url: str) -> None:
        """
        Navigate to specified URL.

        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
        # Auto-screenshot after navigation
        self._auto_screenshot("navigate_to", url.split('//')[-1][:30])

    def is_element_visible(self, locator: Tuple, timeout: int = 5) -> bool:
        """
        Check if element is visible.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: Tuple, timeout: int = 5) -> bool:
        """
        Check if element is present in DOM.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_enabled(self, locator: Tuple, timeout: int = 5) -> bool:
        """
        Check if element is enabled.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if enabled, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_selected(self, locator: Tuple, timeout: int = 5) -> bool:
        """
        Check if element is selected (checkbox/radio).

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            True if selected, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_selected()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_element_text(self, locator: Tuple, timeout: int = 10) -> str:
        """
        Get text content of element.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds

        Returns:
            Element text content

        Raises:
            TimeoutException: If element not found within timeout
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.text

    def get_element_attribute(self, locator: Tuple, attribute: str, timeout: int = 10) -> Optional[str]:
        """
        Get attribute value of element.

        Args:
            locator: Tuple of (By.TYPE, "value")
            attribute: Attribute name to retrieve
            timeout: Maximum wait time in seconds

        Returns:
            Attribute value or None if not found
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute)
        except (TimeoutException, NoSuchElementException):
            return None

    def verify_page_title(self, expected_title: str, timeout: int = 10) -> bool:
        """
        Verify page title matches expected value.

        Args:
            expected_title: Expected page title
            timeout: Maximum wait time in seconds

        Returns:
            True if title matches, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_is(expected_title)
            )
            return True
        except TimeoutException:
            return False

    def verify_page_title_contains(self, partial_title: str, timeout: int = 10) -> bool:
        """
        Verify page title contains expected text.

        Args:
            partial_title: Expected partial title text
            timeout: Maximum wait time in seconds

        Returns:
            True if title contains text, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.title_contains(partial_title)
            )
            return True
        except TimeoutException:
            return False

    def verify_url_contains(self, expected_url: str, timeout: int = 10) -> bool:
        """
        Verify current URL contains expected text.

        Args:
            expected_url: Expected URL fragment
            timeout: Maximum wait time in seconds

        Returns:
            True if URL contains text, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(expected_url)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current URL string
        """
        return self.driver.current_url

    def hover_over_element(self, locator: Tuple, timeout: int = 10) -> None:
        """
        Hover mouse over element.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        # Auto-screenshot after hover
        element_name = str(locator[1])[:30] if len(locator) > 1 else "element"
        self._auto_screenshot("hover", element_name)

    def double_click_element(self, locator: Tuple, timeout: int = 10) -> None:
        """
        Double-click an element.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        # Auto-screenshot after double-click
        element_name = str(locator[1])[:30] if len(locator) > 1 else "element"
        self._auto_screenshot("double_click", element_name)

    def press_key(self, locator: Tuple, key, timeout: int = 10) -> None:
        """
        Press keyboard key on element.

        Args:
            locator: Tuple of (By.TYPE, "value")
            key: Keyboard key from Keys class (e.g., Keys.ENTER)
            timeout: Maximum wait time in seconds
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        element.send_keys(key)
        # Auto-screenshot after key press
        element_name = str(locator[1])[:30] if len(locator) > 1 else "element"
        self._auto_screenshot("press_key", element_name)

    def switch_to_iframe(self, locator: Tuple, timeout: int = 10) -> None:
        """
        Switch driver context to iframe.

        Args:
            locator: Tuple of (By.TYPE, "value")
            timeout: Maximum wait time in seconds
        """
        iframe = WebDriverWait(self.driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(locator)
        )
        # Auto-screenshot after switching to iframe
        element_name = str(locator[1])[:30] if len(locator) > 1 else "iframe"
        self._auto_screenshot("switch_to_iframe", element_name)

    def switch_to_default_content(self) -> None:
        """Switch driver context back to main page."""
        self.driver.switch_to.default_content()

    def refresh_page(self) -> None:
        """Refresh current page."""
        self.driver.refresh()
        # Auto-screenshot after page refresh
        self._auto_screenshot("refresh_page")

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.driver.back()
        # Auto-screenshot after navigation back
        self._auto_screenshot("go_back")

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.driver.forward()
        # Auto-screenshot after navigation forward
        self._auto_screenshot("go_forward")

    def execute_javascript(self, script: str, *args):
        """
        Execute JavaScript in browser.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script

        Returns:
            Script execution result
        """
        return self.driver.execute_script(script, *args)

    def get_page_source(self) -> str:
        """
        Get page HTML source.

        Returns:
            Page source HTML
        """
        return self.driver.page_source
